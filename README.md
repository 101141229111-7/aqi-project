# AQI Prediction Project 🌿

A Flask-based web application that predicts the **Air Quality Index (AQI)** using a machine learning model trained on pollutant data. It supports both automatic and manual input modes, displays interactive data visualizations, and sends email alerts when air quality is unhealthy.

---

## Features

- 🔮 **AQI Prediction** – Predicts AQI from pollutant readings (PM2.5, PM10, NO2, SO2, CO, O3)
- 📊 **Interactive Graphs** – Visualizes AQI trends, average pollutant levels, and PM2.5 vs AQI scatter plots using Plotly
- ⚠️ **Email Alerts** – Sends an automated email notification when AQI exceeds 150 (Unhealthy range)
- 🟢 **AQI Categories** – Color-coded output: Good, Moderate, Unhealthy, Poor, Hazardous
- 🖥️ **Manual Input Mode** – Submit custom pollutant values via a web form

---

## AQI Categories

| AQI Range | Category   | Advice                    | Color    |
|-----------|------------|---------------------------|----------|
| 0 – 50    | Good       | Safe to go outside        | Green    |
| 51 – 100  | Moderate   | Be cautious               | Orange   |
| 101 – 200 | Unhealthy  | Wear mask                 | Red      |
| 201 – 300 | Poor       | Avoid outdoor activities  | Dark Red |
| 300+      | Hazardous  | Stay indoors              | Black    |

---

## Project Structure

```
aqi-project/
├── backend/                     # Flask API — deploy on Render
│   ├── app.py                   # JSON API (prediction, graphs, email alert)
│   ├── model.pkl                # Pre-trained ML model (scikit-learn)
│   ├── cleaned_aqi_dataset.csv  # Dataset used for visualizations
│   ├── requirements.txt         # Python dependencies
│   ├── Procfile                 # Gunicorn startup command
│   └── render.yaml              # Render deployment configuration
└── frontend/                    # Static site — deploy on Vercel
    ├── index.html               # Main prediction page (calls backend API)
    ├── graph.html               # Graph/visualization page (calls backend API)
    └── vercel.json              # Vercel deployment configuration
```

---

## Getting Started (Local Development)

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/101141229111-7/aqi-project.git
   cd aqi-project
   ```

2. **Start the backend**

   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

3. **Open the frontend**

   Open `frontend/index.html` in your browser, or serve it with any static server:

   ```bash
   cd frontend
   python -m http.server 8080
   ```

   > **Note:** Update `BACKEND_URL` in `index.html` and `graph.html` to `http://127.0.0.1:5000` for local development.

---

## Usage

### Auto Mode (Home Page)
Visit `/` to see an AQI prediction using default pollutant values.

### Manual Input Mode
Submit custom pollutant readings via the form on the home page. The form posts to `/predict`.

### Graph Page
Visit `/graph` to view interactive charts:
- AQI trend over time
- Average pollutant bar chart
- PM2.5 vs AQI scatter plot

---

## Deployment

### Backend → Render

1. Go to [render.com](https://render.com) → **New Web Service**
2. Connect your repository and set the **Root Directory** to `backend`
3. Render will auto-detect the `render.yaml` and configure the service
4. Add the following **Environment Variables** in the Render dashboard:
   - `ALERT_EMAIL_SENDER` – Gmail address used to send alerts
   - `ALERT_EMAIL_RECEIVER` – Email address to receive alerts
   - `ALERT_EMAIL_PASSWORD` – Gmail App Password ([how to create one](https://support.google.com/accounts/answer/185833))
5. Copy your Render service URL (e.g. `https://aqi-backend.onrender.com`)

### Frontend → Vercel

1. Open `frontend/index.html` and `frontend/graph.html`
2. Replace `https://your-backend.onrender.com` with your actual Render URL in both files
3. Go to [vercel.com](https://vercel.com) → **New Project**
4. Connect your repository and set the **Root Directory** to `frontend`
5. Deploy — Vercel will serve the static files automatically

---

## Dependencies

| Package       | Purpose                        |
|---------------|--------------------------------|
| Flask         | Web framework                  |
| flask-cors    | Cross-Origin Resource Sharing  |
| pandas        | Data manipulation              |
| scikit-learn  | Machine learning model         |
| plotly        | Interactive data visualizations|
| gunicorn      | Production WSGI server         |

---

## License

This project is open-source and available for educational purposes.
