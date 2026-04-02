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
├── app.py                   # Flask application (routes, prediction, email alert)
├── model.pkl                # Pre-trained ML model (scikit-learn)
├── cleaned_aqi_dataset.csv  # Dataset used for visualizations
├── index.html               # Main prediction page template
├── graph.html               # Graph/visualization page template
├── requirements.txt         # Python dependencies
├── Procfile                 # Gunicorn startup command (Heroku/Render)
└── vercel.json              # Vercel deployment configuration
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/101141229111-7/aqi-project.git
   cd aqi-project
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   python app.py
   ```

4. Open your browser and navigate to `http://127.0.0.1:5000`

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

### Heroku / Render
The `Procfile` is configured to run with Gunicorn:
```
web: gunicorn app:app
```

### Vercel
The `vercel.json` routes all requests to the app entry point.

---

## Dependencies

| Package       | Purpose                        |
|---------------|--------------------------------|
| Flask         | Web framework                  |
| pandas        | Data manipulation              |
| scikit-learn  | Machine learning model         |
| plotly        | Interactive data visualizations|
| gunicorn      | Production WSGI server         |

---

## License

This project is open-source and available for educational purposes.
