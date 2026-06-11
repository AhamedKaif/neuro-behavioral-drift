"""
Backend API Smoke Test
Runs a complete end-to-end flow:
  1. Register a new test user
  2. Login to verify auth
  3. Submit behavioral metrics (normal + fatigued)
  4. Fetch dashboard data
  5. Fetch alerts
  6. Fetch model info
"""
import json
import sys
import os
import requests

BASE = "http://localhost:5000"
TEST_USER = {"username": "smoketest_user", "password": "testpass123"}

def colored(text, code):
    return f"\033[{code}m{text}\033[0m"

def ok(msg):   print(colored(f"  ✅ {msg}", "32"))
def fail(msg): print(colored(f"  ❌ {msg}", "31")); sys.exit(1)
def info(msg): print(colored(f"  ℹ  {msg}", "36"))

def run():
    print(colored("\n🧠 Neuro-Behavioral Drift — Backend Smoke Test", "1;34"))
    print("=" * 50)
    token = None

    # 1. Register
    print(colored("\n[1] Auth — Register", "33"))
    r = requests.post(f"{BASE}/api/auth/register", json=TEST_USER)
    if r.status_code in (201, 409):  # 409 = already exists, still ok
        if r.status_code == 201:
            token = r.json()["token"]
            ok(f"Registered new user: {TEST_USER['username']}")
        else:
            info("User already exists — proceeding to login")
    else:
        fail(f"Register failed: {r.status_code} {r.text}")

    # 2. Login
    print(colored("\n[2] Auth — Login", "33"))
    r = requests.post(f"{BASE}/api/auth/login", json=TEST_USER)
    if r.status_code == 200:
        token = r.json()["token"]
        ok(f"Login successful. Token: {token[:30]}...")
    else:
        fail(f"Login failed: {r.status_code} {r.text}")

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Verify /me
    print(colored("\n[3] Auth — /me", "33"))
    r = requests.get(f"{BASE}/api/auth/me", headers=headers)
    if r.status_code == 200:
        ok(f"Current user: {r.json()['username']}")
    else:
        fail(f"/me failed: {r.status_code} {r.text}")

    # 4. Submit normal metrics
    print(colored("\n[4] Metrics — Submit (Normal)", "33"))
    normal_metrics = {
        "screen_time": 180.0,
        "typing_speed": 260.0,
        "typing_error_rate": 0.03,
        "session_duration": 25.0,
        "click_frequency": 30.0,
        "break_frequency": 2.5,
        "mouse_speed": 420.0,
    }
    r = requests.post(f"{BASE}/api/metrics", json=normal_metrics, headers=headers)
    if r.status_code == 201:
        data = r.json()
        pred = data["prediction"]
        ok(f"Strain: {pred['strain_label']} | Drift: {pred['drift_score']}% | Confidence: {round(pred['probability']*100)}%")
        info(f"Alerts generated: {len(data['alerts'])}")
    else:
        fail(f"Metrics ingest failed: {r.status_code} {r.text}")

    # 5. Submit fatigued metrics
    print(colored("\n[5] Metrics — Submit (Fatigue Simulation)", "33"))
    fatigued_metrics = {
        "screen_time": 540.0,
        "typing_speed": 95.0,
        "typing_error_rate": 0.22,
        "session_duration": 140.0,
        "click_frequency": 8.0,
        "break_frequency": 0.2,
        "mouse_speed": 80.0,
    }
    r = requests.post(f"{BASE}/api/metrics", json=fatigued_metrics, headers=headers)
    if r.status_code == 201:
        data = r.json()
        pred = data["prediction"]
        ok(f"Strain: {pred['strain_label']} | Drift: {pred['drift_score']}% | Confidence: {round(pred['probability']*100)}%")
        alert_types = [a['type'] for a in data['alerts']]
        info(f"Alerts: {', '.join(alert_types) if alert_types else 'None'}")
        if pred['strain_label'] != 'High':
            print(colored("  ⚠ Expected 'High' strain for fatigue simulation", "33"))
    else:
        fail(f"Fatigued metrics ingest failed: {r.status_code} {r.text}")

    # 6. Dashboard
    print(colored("\n[6] Dashboard Data", "33"))
    r = requests.get(f"{BASE}/api/dashboard", headers=headers)
    if r.status_code == 200:
        data = r.json()
        ok(f"Timeseries records: {len(data.get('timeseries', []))}")
        if data.get('latest_prediction'):
            ok(f"Latest prediction: {data['latest_prediction']['strain_label']}")
    else:
        fail(f"Dashboard failed: {r.status_code} {r.text}")

    # 7. Alerts
    print(colored("\n[7] Alerts", "33"))
    r = requests.get(f"{BASE}/api/alerts", headers=headers)
    if r.status_code == 200:
        ok(f"Active alerts count: {len(r.json())}")
    else:
        fail(f"Alerts failed: {r.status_code} {r.text}")

    # 8. Model Info
    print(colored("\n[8] Model Info", "33"))
    r = requests.get(f"{BASE}/api/model/info", headers=headers)
    if r.status_code == 200:
        ok(f"Model accuracy: {r.json()['accuracy'] * 100:.1f}%")
    else:
        fail(f"Model info failed: {r.status_code} {r.text}")

    print(colored("\n" + "=" * 50, "32"))
    print(colored("  🎉 All smoke tests passed! Backend is healthy.\n", "1;32"))

if __name__ == "__main__":
    try:
        run()
    except requests.ConnectionError:
        print(colored(
            "\n❌ Could not connect to Flask server at http://localhost:5000\n"
            "   Make sure the backend is running: python backend/app.py\n", "31"
        ))
        sys.exit(1)
