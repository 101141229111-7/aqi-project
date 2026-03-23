import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load model
model = pickle.load(open('model.pkl', 'rb'))

def send_email_alert(aqi_value):
    sender_email = "janu012006@gmail.com"
    receiver_email = "janu012006@gmail.com"
    password = "rbwomtistqwtpasf"

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

# 🔥 AUTO MODE (without input)
@app.route('/')
def home():
    pm25 = 80
    pm10 = 90
    no2 = 100
    so2 = 70
    co = 1
    o3 = 80

    sample = pd.DataFrame([[pm25, pm10, no2, so2, co, o3]],
    columns=["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"])

    prediction = model.predict(sample)[0]

    # ✅ FIXED POSITION
    alert = None
    if prediction > 150:
        alert = "⚠️ Air Quality is Unhealthy!"
        send_email_alert(prediction)

    # CATEGORY LOGIC
    if prediction <= 50:
        category = "Good"
        message = "Safe to go outside"
        color = "green"
    elif prediction <= 100:
        category = "Moderate"
        message = "Be cautious"
        color = "orange"
    elif prediction <= 200:
        category = "Unhealthy"
        message = "Wear mask"
        color = "red"
    elif prediction <= 300:
        category = "Poor"
        message = "Avoid outdoor activities"
        color = "darkred"
    else:
        category = "Hazardous"
        message = "Stay indoors"
        color = "black"

    return render_template('index.html',
                           category=category,
                           message=message,
                           color=color,
                           alert=alert)


# 🔥 MANUAL INPUT MODE
@app.route('/predict', methods=['POST'])
def predict():
    pm25 = float(request.form['pm25'])
    pm10 = float(request.form['pm10'])
    no2 = float(request.form['no2'])
    so2 = float(request.form['so2'])
    co = float(request.form['co'])
    o3 = float(request.form['o3'])

    sample = pd.DataFrame([[pm25, pm10, no2, so2, co, o3]],
    columns=["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"])

    prediction = model.predict(sample)[0]

    # ✅ FIXED (ADDED EMAIL CALL)
    alert = None
    if prediction > 150:
        alert = "⚠️ Air Quality is Unhealthy!"
        send_email_alert(prediction)

    # CATEGORY LOGIC
    if prediction <= 50:
        category = "Good"
        message = "Safe to go outside"
        color = "green"
    elif prediction <= 100:
        category = "Moderate"
        message = "Be cautious"
        color = "orange"
    elif prediction <= 200:
        category = "Unhealthy"
        message = "Wear mask"
        color = "red"
    elif prediction <= 300:
        category = "Poor"
        message = "Avoid outdoor activities"
        color = "darkred"
    else:
        category = "Hazardous"
        message = "Stay indoors"
        color = "black"

    return render_template('index.html',
                           category=category,
                           message=message,
                           color=color,
                           alert=alert)


# 🔥 GRAPH PAGE
@app.route("/graph")
def graph():
    import plotly.graph_objects as go
    import plotly.express as px

    data = pd.read_csv("cleaned_aqi_dataset.csv")

    # 1️⃣ AQI LINE GRAPH
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(y=data["AQI"], mode='lines', name="AQI"))
    graph1 = fig1.to_html(full_html=False)

    # 2️⃣ POLLUTANTS BAR GRAPH
    avg_values = data[["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]].mean()
    fig2 = px.bar(x=avg_values.index, y=avg_values.values,
                  labels={'x': 'Pollutants', 'y': 'Average Value'},
                  title="Average Pollutant Levels")
    graph2 = fig2.to_html(full_html=False)

    # 3️⃣ SCATTER GRAPH
    fig3 = px.scatter(data, x="PM2.5", y="AQI",
                      title="PM2.5 vs AQI Relationship")
    graph3 = fig3.to_html(full_html=False)

    return render_template("graph.html",
                           graph1=graph1,
                           graph2=graph2,
                           graph3=graph3)

if __name__ == "__main__":
    app.run(debug=True)
