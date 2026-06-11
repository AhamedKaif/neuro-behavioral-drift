# Neuro-Behavioral Drift Modeling for Early Cognitive Strain Detection

This project is a full-stack, machine learning-powered web application designed to monitor user interaction patterns (keystrokes, mouse movement, active sessions, and rest cycles) to detect early indicators of cognitive strain and fatigue.

---

## 🏗️ Architecture Overview

The system consists of three main modules:
1. **Frontend (React + Tailwind CSS + Recharts)**: Captures user interaction telemetry (typing speed, correction rates, click frequencies, mouse speed) and serves a highly interactive monitoring dashboard complete with live tracking, weekly trends, and fatigue simulation.
2. **Backend (Python Flask + SQLite/PostgreSQL-compatible DB)**: Stores behavioral timeseries logs, user session accounts, and recommendations. Exposes RESTful endpoints for metrics collection and queries.
3. **Machine Learning Model (Scikit-Learn Random Forest)**: Predicts cognitive strain level (Low, Medium, High) based on behavioral features and computes custom user behavioral drift metrics.

---

## 🗄️ Database Schema

The SQLite schema is structured to mirror PostgreSQL specifications for production migration:

### 1. `users` Table
- `id` (INTEGER / SERIAL PRIMARY KEY)
- `username` (VARCHAR UNIQUE NOT NULL)
- `password_hash` (VARCHAR NOT NULL)
- `created_at` (TIMESTAMP)

### 2. `behavioral_metrics` Table
- `id` (INTEGER / SERIAL PRIMARY KEY)
- `user_id` (INTEGER REFERENCES users)
- `timestamp` (TIMESTAMP)
- `screen_time` (REAL) - Daily cumulative screen minutes
- `typing_speed` (REAL) - Keystrokes per minute (CPM)
- `typing_error_rate` (REAL) - Ratio of Backspaces/Deletes to total keys
- `session_duration` (REAL) - Active continuous session length in minutes
- `click_frequency` (REAL) - Click rates per minute
- `break_frequency` (REAL) - Breaks per hour
- `mouse_speed` (REAL) - Mouse movement speed in pixels/second

### 3. `predictions` Table
- `id` (INTEGER / SERIAL PRIMARY KEY)
- `user_id` (INTEGER REFERENCES users)
- `timestamp` (TIMESTAMP)
- `drift_score` (REAL) - Deviation from baseline profile (0-100%)
- `strain_label` (VARCHAR) - `Low`, `Medium`, or `High`
- `strain_probability` (REAL) - Model confidence probability

### 4. `system_alerts` Table
- `id` (INTEGER / SERIAL PRIMARY KEY)
- `user_id` (INTEGER REFERENCES users)
- `timestamp` (TIMESTAMP)
- `alert_type` (VARCHAR) - e.g. `HIGH_STRAIN`, `LONG_SESSION`, `BREAK_REMINDER`
- `message` (TEXT)
- `is_read` (INTEGER/BOOLEAN)

---

## 🧠 Machine Learning Engine

The ML classifier accepts a 7-dimensional behavioral feature vector and predicts one of three cognitive strain classes:
- **Low Cognitive Strain (0)**: Alert state. High/moderate typing speed, low backspace correction rate, regular rest breaks.
- **Medium Cognitive Strain (1)**: Moderate fatigue. Steady decrease in typing speed, elevated error corrections, and extended active sessions.
- **High Cognitive Strain (2)**: Heavy exhaustion / behavioral drift. Sluggish or erratic typing (low CPM), high backspace corrections, prolonged work session, and sluggish mouse speed.

A **Behavioral Drift Score** is calculated alongside prediction by computing the deviation of the current features against the user's personal calibrated baseline (average of metrics recorded when strain level is `Low`).

---

## 🚀 Setup & Installation

### 1. Clone the project and configure the Active Workspace
Ensure you open the project directory in your IDE as the active workspace:
```bash
cd C:\Users\ahame\.gemini\antigravity\scratch\neuro-behavioral-drift
```

### 2. Backend Setup (Flask)
Python 3.8+ is required.
```bash
cd backend
# Create virtual environment
python -m venv venv
# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Train Machine Learning Model
Generate dataset and train classifier:
```bash
cd ../ml-model
python train.py
```
This trains the Random Forest classifier and exports `strain_classifier.joblib` and `scaler.joblib`.

### 4. Run Backend Server
```bash
cd ../backend
python app.py
```
The backend will boot up on `http://localhost:5000` and automatically initialize the SQLite database (`database/database.db`).

### 5. Frontend Setup (React)
Node.js is required.
```bash
cd ../frontend
# Install dependencies
npm install

# Run Vite development server
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 🛠️ Testing the Application

1. **Register/Login**: Open the page, register a new user, and log in.
2. **Calibrate/Test Sandbox**:
   - In the **Interactive Behavioral Sandbox**, start moving your cursor and typing text.
   - Click the "Transmit Metrics to Model" button to record this data.
3. **Simulate Fatigue**:
   - Check the **Force Cognitive Fatigue Simulation** checkbox on the dashboard.
   - Click "Transmit Metrics to Model".
   - The dashboard will refresh to display a **High Cognitive Strain** status, a high **Behavioral Drift Score**, and trigger active **Recommendations** (break reminders) in the alerts feed!
