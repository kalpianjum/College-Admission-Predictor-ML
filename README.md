# 🎓 College Admission Predictor

A full-stack, machine learning-powered web application designed to predict the best-fitting colleges/institutions for students based on their exam rank, category, desired branch, and region (specifically built for AP EAPCET 2023 data).

## 🏛 Architecture Overview
This project uses a modern microservices-style architecture, decoupling the user interface, backend routing, and the machine learning model.

1. **Frontend (React.js)**: A responsive user interface where students input their details and view matching colleges.
2. **Backend Gateway (Express.js / Node.js)**: A lightweight API layer that handles requests from the React frontend, prevents direct exposure of the ML model, and proxies prediction requests via `axios`.
3. **Machine Learning Model (Flask / Scikit-Learn)**: A Python service that implements a `RandomForestRegressor`. It cleans the input data dynamically, encodes the categories, processes the prediction, and uses distance logic to serve the top 2 matching institutions based on historical cutoffs and fee information.

## 🚀 Tech Stack
* **Frontend**: React.js, Fetch API
* **Backend**: Node.js, Express.js, Cors, Body-Parser
* **Machine Learning**: Python 3, Flask, Scikit-Learn, Pandas, Numpy

---

## 🛠️ How to Run Locally

### Prerequisites
Make sure you have [Node.js](https://nodejs.org/) and [Python 3](https://www.python.org/downloads/) installed on your machine.

### 1. Start the Machine Learning API (Flask)
```bash
cd ml-model
pip install -r requirements.txt
python model.py
```
*The Flask server will start on `http://localhost:5000`.*

### 2. Start the Backend Proxy API (Express)
Open a **new terminal tab/window**:
```bash
cd backend
npm install
npm start
```
*The Express server will start on `http://localhost:4000`.*

### 3. Start the Frontend Application (React)
Open a **third terminal tab/window**:
```bash
cd frontend
npm install
npm start
```
*The React application will automatically open in your browser at `http://localhost:3000`.*

---

## 🌎 Deployment Setup (Cloud)
This repository is configured to be deployed on modern cloud platforms using environment variables to wire the microservices together.

### Relevant Environment Variables
If you are deploying this application, you must configure the following environment variables in your cloud provider:

**Frontend (e.g., Vercel / Netlify)**
- `REACT_APP_API_URL`: The URL of your deployed Express backend (e.g. `https://my-backend.onrender.com`).

**Backend (e.g., Render / Heroku)**
- `FLASK_API_URL`: The URL of your deployed Flask ML service (e.g. `https://ml-model-xyz.onrender.com`).
- `FRONTEND_URL`: The URL of your deployed React application (e.g. `https://my-frontend.vercel.app`).

**ML Model (e.g., Render)**
- `EXPRESS_BACKEND_URL`: The URL of your deployed Express backend (e.g. `https://my-backend.onrender.com`).
- `PORT`: (Auto-injected by most providers).

---

## 📁 Project Structure
```text
project/
├── frontend/                     # React User Interface
│   ├── src/
│   │   └── App.js                # Main React logic mapping inputs & displaying UI
│   └── package.json              
├── backend/                      # Express API Gateway
│   ├── server.js                 # Proxy server intercepting /api/predict
│   └── package.json              
├── ml-model/                     # Machine Learning Service (Flask)
│   ├── model.py                  # Random Forest training & Flask routes
│   └── requirements.txt          # Python dependencies (incl. gunicorn for production)
├── APEAPCET2023LASTRANKDETAILS.csv  # Dataset used for training
└── project1.py                   # Testing CLI script for ML logic
```
