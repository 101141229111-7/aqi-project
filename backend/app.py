import os
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

app = Flask(__name__)
CORS(app)

# Load model and dataset at startup
model = pickle.load(open('model.pkl', 'rb'))
aqi_data = pd.read_csv("cleaned_aqi_dataset.csv")


def send_email_alert(aqi_value):
    sender_email = os.environ.get("ALERT_EMAIL_SENDER", "")
    receiver_email = os.environ.get("ALERT_EMAIL_RECEIVER", "")
    password = os.environ.get("ALERT_EMAIL_PASSWORD", "")

    if not sender_email or not password:
        print("Email credentials not configured, skipping alert.")
        return

    message = f"⚠️ Alert! AQI Level is {aqi_value}. Air quality is unhealthy. Please take precautions."

    msg = MIMEText(message)
    msg["Subject"] = "AQI Alert Notification"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("✅ Email sent successfully")
    except Exception as e:
        print("❌ Error:", e)


def categorize(prediction):
    alert = None
    if prediction > 150:
        alert = "⚠️ Air Quality is Unhealthy!"
        send_email_alert(prediction)

    if prediction <= 50:
        category, message, color = "Good", "Safe to go outside", "green"
    elif prediction <= 100:
        category, message, color = "Moderate", "Be cautious", "orange"
    elif prediction <= 200:
        category, message, color = "Unhealthy", "Wear mask", "red"
    elif prediction <= 300:
        category, message, color = "Poor", "Avoid outdoor activities", "darkred"
    else:
        category, message, color = "Hazardous", "Stay indoors", "black"

    return {"category": category, "message": message, "color": color, "alert": alert, "aqi": round(float(prediction), 2)}


# Default prediction
@app.route('/')
def home():
    sample = pd.DataFrame([[80, 90, 100, 70, 1, 80]],
                          columns=["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"])
    prediction = model.predict(sample)[0]
    return jsonify(categorize(prediction))


# Manual input prediction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    required_fields = ['pm25', 'pm10', 'no2', 'so2', 'co', 'o3']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        pm25 = float(data['pm25'])
        pm10 = float(data['pm10'])
        no2 = float(data['no2'])
        so2 = float(data['so2'])
        co = float(data['co'])
        o3 = float(data['o3'])
    except (ValueError, TypeError):
        return jsonify({"error": "All fields must be numeric values"}), 400

    sample = pd.DataFrame([[pm25, pm10, no2, so2, co, o3]],
                          columns=["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"])
    prediction = model.predict(sample)[0]
    return jsonify(categorize(prediction))


# Graph data
@app.route('/graph')
def graph():
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(y=aqi_data["AQI"], mode='lines', name="AQI"))
    graph1 = fig1.to_html(full_html=False)

    avg_values = aqi_data[["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]].mean()
    fig2 = px.bar(x=avg_values.index, y=avg_values.values,
                  labels={'x': 'Pollutants', 'y': 'Average Value'},
                  title="Average Pollutant Levels")
    graph2 = fig2.to_html(full_html=False)

    fig3 = px.scatter(aqi_data, x="PM2.5", y="AQI",
                      title="PM2.5 vs AQI Relationship")
    graph3 = fig3.to_html(full_html=False)

    return jsonify({"graph1": graph1, "graph2": graph2, "graph3": graph3})


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug)
