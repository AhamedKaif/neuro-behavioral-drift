import json
import random
import os

def generate_scenarios():
    scenarios = []
    tc_counter = 1

    def add_case(api, method, name, category, expected_status, requires_auth, payload=None, params=None, headers=None):
        nonlocal tc_counter
        scenarios.append({
            "id": f"TC-{tc_counter:03d}",
            "api": api,
            "method": method,
            "name": name,
            "category": category,
            "expected_status": expected_status,
            "requires_auth": requires_auth,
            "payload": payload,
            "params": params,
            "headers": headers
        })
        tc_counter += 1

    # 1. Registration Scenarios (50 cases)
    # Valid registration cases
    occupations = ["Student", "Developer", "Researcher", "Engineer", "Manager", "Designer"]
    institutions = ["Stanford", "MIT", "Harvard", "UC Berkeley", "Oxford", "Cambridge"]
    departments = ["Computer Science", "Biology", "Psychology", "Neuroscience", "Physics"]
    
    for i in range(25):
        username = f"user_reg_{i}_{random.randint(1000, 9999)}"
        email = f"{username}@test.com"
        payload = {
            "full_name": f"Reg User {i}",
            "username": username,
            "email": email,
            "password": "ValidPassword123!",
            "age": random.randint(18, 65),
            "gender": random.choice(["Male", "Female", "Non-binary", "Prefer not to say"]),
            "occupation": random.choice(occupations),
            "institution": random.choice(institutions),
            "department": random.choice(departments),
            "academic_year": random.choice(["1st Year", "2nd Year", "3rd Year", "4th Year", "N/A"]),
            "working_hours": round(random.uniform(4.0, 12.0), 1),
            "avg_screen_time": round(random.uniform(2.0, 10.0), 1),
            "avg_sleep_hours": round(random.uniform(5.0, 9.0), 1),
            "preferred_work_time": random.choice(["Morning", "Afternoon", "Night", "Flexible"]),
            "stress_level": random.randint(1, 10)
        }
        add_case("/api/auth/register", "POST", f"Valid Registration - {payload['occupation']}", "positive", 201, False, payload)

    # Invalid registration cases (negative and boundary)
    add_case("/api/auth/register", "POST", "Registration - Missing Username", "negative", 400, False, {
        "full_name": "No Username", "email": "nousername@test.com", "password": "pass"
    })
    add_case("/api/auth/register", "POST", "Registration - Missing Password", "negative", 400, False, {
        "full_name": "No Password", "username": "nopass", "email": "nopass@test.com"
    })
    add_case("/api/auth/register", "POST", "Registration - Missing Email", "negative", 400, False, {
        "full_name": "No Email", "username": "noemail", "password": "pass"
    })
    add_case("/api/auth/register", "POST", "Registration - Missing Full Name", "negative", 400, False, {
        "username": "nofullname", "email": "nofullname@test.com", "password": "pass"
    })
    # Boundary / Invalid inputs
    add_case("/api/auth/register", "POST", "Registration - Age Boundary (Underage)", "boundary", 201, False, {
        "full_name": "Underage", "username": "underage_user", "email": "underage@test.com", "password": "pass", "age": 5
    })
    add_case("/api/auth/register", "POST", "Registration - Stress Level Boundary (Low)", "boundary", 201, False, {
        "full_name": "Stress Low", "username": "stress_low_user", "email": "stress_low@test.com", "password": "pass", "stress_level": 1
    })
    add_case("/api/auth/register", "POST", "Registration - Stress Level Boundary (High)", "boundary", 201, False, {
        "full_name": "Stress High", "username": "stress_high_user", "email": "stress_high@test.com", "password": "pass", "stress_level": 10
    })
    add_case("/api/auth/register", "POST", "Registration - Invalid Stress Level (Too High)", "negative", 400, False, {
        "full_name": "Stress Invalid", "username": "stress_inv_user", "email": "stress_inv@test.com", "password": "pass", "stress_level": 11
    })
    add_case("/api/auth/register", "POST", "Registration - Invalid Stress Level (Too Low)", "negative", 400, False, {
        "full_name": "Stress Invalid 2", "username": "stress_inv_user2", "email": "stress_inv2@test.com", "password": "pass", "stress_level": 0
    })
    
    # Rest of the registration negative cases to reach 50
    for i in range(16):
        add_case("/api/auth/register", "POST", f"Registration - Invalid Data Type {i}", "negative", 400, False, {
            "full_name": "Bad Type", "username": f"bad_type_{i}", "email": f"bad_type_{i}@test.com", "password": "pass",
            "stress_level": "very stressed" if i % 2 == 0 else [1, 2],
            "age": "twenty" if i % 2 == 1 else None
        })

    # 2. Login Scenarios (40 cases)
    # Valid logins
    for i in range(15):
        add_case("/api/auth/login", "POST", f"Valid Login - Case {i}", "positive", 200, False, {
            "username": f"user_login_{i}", # We will dynamically match or create these in the script
            "password": "ValidPassword123!"
        })
    # Invalid logins (wrong password, wrong user, empty, injection, etc.)
    for i in range(10):
        add_case("/api/auth/login", "POST", f"Invalid Login - Wrong Password {i}", "negative", 401, False, {
            "username": f"user_login_{i}", "password": f"wrongpassword_{i}"
        })
    for i in range(10):
        add_case("/api/auth/login", "POST", f"Invalid Login - Nonexistent User {i}", "negative", 401, False, {
            "username": f"nonexistent_{i}_{random.randint(1000, 9999)}", "password": "some_password"
        })
    add_case("/api/auth/login", "POST", "Login - Empty Username", "negative", 400, False, {"username": "", "password": "pwd"})
    add_case("/api/auth/login", "POST", "Login - Empty Password", "negative", 400, False, {"username": "user", "password": ""})
    add_case("/api/auth/login", "POST", "Login - Missing Fields", "negative", 400, False, {})
    add_case("/api/auth/login", "POST", "Login - SQL Injection Attempt", "negative", 401, False, {"username": "' OR '1'='1", "password": "pwd"})
    add_case("/api/auth/login", "POST", "Login - Special Characters in Username", "negative", 401, False, {"username": "user!@#$%", "password": "pwd"})

    # 3. Auth Me Scenarios (30 cases)
    # Positive
    for i in range(10):
        add_case("/api/auth/me", "GET", f"Get Current User - Valid Token {i}", "positive", 200, True)
    # Negative / Unauthorized (expired, invalid, missing tokens)
    add_case("/api/auth/me", "GET", "Get Current User - No Token", "negative", 401, False)
    add_case("/api/auth/me", "GET", "Get Current User - Expired Token", "negative", 401, False, headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6IjEiLCJleHAiOjE2MDAwMDAwMDB9.invalid"})
    add_case("/api/auth/me", "GET", "Get Current User - Malformed Token", "negative", 401, False, headers={"Authorization": "Bearer malformed_token_string"})
    add_case("/api/auth/me", "GET", "Get Current User - Wrong Schema", "negative", 401, False, headers={"Authorization": "Basic YWRtaW46YWRtaW4="})
    for i in range(16):
        add_case("/api/auth/me", "GET", f"Get Current User - Unauthorized Probe {i}", "negative", 401, False, headers={"Authorization": f"Bearer fake_token_{i}"})

    # 4. Profile GET/PUT Scenarios (40 cases)
    # GET Profile
    for i in range(10):
        add_case("/api/profile", "GET", f"Get Profile - Case {i}", "positive", 200, True)
    add_case("/api/profile", "GET", "Get Profile - No Token", "negative", 401, False)
    add_case("/api/profile", "GET", "Get Profile - Bad Token", "negative", 401, False, headers={"Authorization": "Bearer bad"})
    
    # PUT Profile
    for i in range(15):
        payload = {
            "full_name": f"Updated Name {i}",
            "age": random.randint(20, 50),
            "working_hours": round(random.uniform(5.0, 10.0), 1),
            "stress_level": random.randint(1, 10)
        }
        add_case("/api/profile", "PUT", f"Update Profile - Valid fields {i}", "positive", 200, True, payload)

    # PUT Profile Invalid/Boundary
    add_case("/api/profile", "PUT", "Update Profile - Invalid Age (Too High)", "boundary", 400, True, {"age": 150})
    add_case("/api/profile", "PUT", "Update Profile - Invalid Age (Negative)", "boundary", 400, True, {"age": -5})
    add_case("/api/profile", "PUT", "Update Profile - Invalid Stress Level (Too High)", "negative", 400, True, {"stress_level": 12}) # Database check constraint might fail
    add_case("/api/profile", "PUT", "Update Profile - Invalid Stress Level (Too Low)", "negative", 400, True, {"stress_level": 0})
    add_case("/api/profile", "PUT", "Update Profile - Invalid working hours type", "negative", 400, True, {"working_hours": "ten"})
    add_case("/api/profile", "PUT", "Update Profile - No payload", "positive", 200, True, {})
    for i in range(7):
        add_case("/api/profile", "PUT", f"Update Profile - Unauthenticated {i}", "negative", 401, False, {"full_name": "Hack"}, headers={"Authorization": f"Bearer fake_{i}"})

    # 5. Delete Account Scenarios (20 cases)
    # Deleting accounts (mostly negative/unauthorized to avoid destroying test pool, plus a few valid)
    for i in range(17):
        add_case("/api/profile/account", "DELETE", f"Delete Account - Unauthenticated {i}", "negative", 401, False, headers={"Authorization": f"Bearer bad_token_{i}"})
    add_case("/api/profile/account", "DELETE", "Delete Account - No Token", "negative", 401, False)
    # Valid delete cases (we will create temporary users for these dynamically)
    add_case("/api/profile/account", "DELETE", "Delete Account - Valid Case 1", "positive", 200, True)
    add_case("/api/profile/account", "DELETE", "Delete Account - Valid Case 2", "positive", 200, True)

    # 6. Notifications Scenarios (60 cases)
    # GET Notifications (different severities)
    for i in range(10):
        severity = random.choice(["ALL", "INFO", "MEDIUM", "HIGH"])
        add_case("/api/notifications", "GET", f"Get Notifications - Severity {severity} {i}", "positive", 200, True, params={"severity": severity})
    add_case("/api/notifications", "GET", "Get Notifications - Invalid Severity", "positive", 200, True, params={"severity": "INVALID"}) # Server should return ALL or default
    add_case("/api/notifications", "GET", "Get Notifications - No Token", "negative", 401, False)
    
    # GET Unread Count
    for i in range(10):
        add_case("/api/notifications/unread-count", "GET", f"Get Unread Count - Case {i}", "positive", 200, True)
    add_case("/api/notifications/unread-count", "GET", "Get Unread Count - No Token", "negative", 401, False)

    # Read All Notifications
    for i in range(10):
        add_case("/api/notifications/read-all", "POST", f"Mark All Notifications Read - Case {i}", "positive", 200, True)
    add_case("/api/notifications/read-all", "POST", "Mark All Notifications Read - No Token", "negative", 401, False)

    # Mark Notification Read (PUT /api/notifications/<id>/read)
    for i in range(12):
        # We will dynamically substitute the notification ID in the K6 script.
        # But we'll test non-existent IDs too
        add_case(f"/api/notifications/{9999 + i}/read", "PUT", f"Mark Read - Nonexistent ID {i}", "negative", 200, True) # SQLite usually returns success or no-op
    add_case("/api/notifications/123/read", "PUT", "Mark Read - No Token", "negative", 401, False)

    # Delete Notification (DELETE /api/notifications/<id>)
    for i in range(12):
        add_case(f"/api/notifications/{9999 + i}", "DELETE", f"Delete Notification - Nonexistent ID {i}", "negative", 200, True)
    add_case("/api/notifications/123", "DELETE", "Delete Notification - No Token", "negative", 401, False)

    # 7. Metrics Ingestion Scenarios (80 cases)
    # Positive - normal behavior (Low strain)
    for i in range(25):
        payload = {
            "screen_time": round(random.uniform(60.0, 180.0), 1),
            "typing_speed": round(random.uniform(200.0, 300.0), 1),
            "typing_error_rate": round(random.uniform(0.01, 0.05), 3),
            "session_duration": round(random.uniform(15.0, 45.0), 1),
            "click_frequency": round(random.uniform(20.0, 40.0), 1),
            "break_frequency": round(random.uniform(1.5, 3.5), 2),
            "mouse_speed": round(random.uniform(300.0, 500.0), 1)
        }
        add_case("/api/metrics", "POST", f"Ingest Metrics - Normal {i}", "positive", 201, True, payload)

    # Positive - fatigue indicators (Medium/High strain, alerts)
    for i in range(25):
        # Fatigued: low speed, high errors, long session, fewer breaks, low mouse speed
        payload = {
            "screen_time": round(random.uniform(400.0, 700.0), 1),
            "typing_speed": round(random.uniform(60.0, 110.0), 1),
            "typing_error_rate": round(random.uniform(0.15, 0.30), 3),
            "session_duration": round(random.uniform(100.0, 180.0), 1),
            "click_frequency": round(random.uniform(5.0, 15.0), 1),
            "break_frequency": round(random.uniform(0.0, 0.4), 2),
            "mouse_speed": round(random.uniform(5.0, 120.0), 1)
        }
        add_case("/api/metrics", "POST", f"Ingest Metrics - Fatigued {i}", "positive", 201, True, payload)

    # Boundary cases
    add_case("/api/metrics", "POST", "Ingest Metrics - Boundary (Zero metrics)", "boundary", 201, True, {
        "screen_time": 0.0, "typing_speed": 0.0, "typing_error_rate": 0.0, "session_duration": 0.0,
        "click_frequency": 0.0, "break_frequency": 0.0, "mouse_speed": 0.0
    })
    add_case("/api/metrics", "POST", "Ingest Metrics - Boundary (Very high values)", "boundary", 201, True, {
        "screen_time": 1440.0, "typing_speed": 1000.0, "typing_error_rate": 1.0, "session_duration": 1440.0,
        "click_frequency": 500.0, "break_frequency": 10.0, "mouse_speed": 5000.0
    })
    
    # Negative cases (missing, invalid types, negative numbers, unauthenticated)
    add_case("/api/metrics", "POST", "Ingest Metrics - Missing Screen Time", "negative", 400, True, {
        "typing_speed": 200.0, "typing_error_rate": 0.02, "session_duration": 30.0,
        "click_frequency": 25.0, "break_frequency": 2.0, "mouse_speed": 400.0
    })
    add_case("/api/metrics", "POST", "Ingest Metrics - Non-numeric Value", "negative", 400, True, {
        "screen_time": "two hours", "typing_speed": 200.0, "typing_error_rate": 0.02, "session_duration": 30.0,
        "click_frequency": 25.0, "break_frequency": 2.0, "mouse_speed": 400.0
    })
    add_case("/api/metrics", "POST", "Ingest Metrics - No Token", "negative", 401, False, {
        "screen_time": 100.0, "typing_speed": 200.0, "typing_error_rate": 0.02, "session_duration": 30.0,
        "click_frequency": 25.0, "break_frequency": 2.0, "mouse_speed": 400.0
    })
    
    # Additional negative metrics cases to reach 80
    for i in range(25):
        add_case("/api/metrics", "POST", f"Ingest Metrics - Negative Values {i}", "boundary", 201, True, {
            "screen_time": -10.0 - i, "typing_speed": 200.0, "typing_error_rate": 0.02, "session_duration": 30.0,
            "click_frequency": 25.0, "break_frequency": 2.0, "mouse_speed": 400.0
        })

    # 8. Dashboard GET Scenarios (40 cases)
    for i in range(30):
        add_case("/api/dashboard", "GET", f"Get Dashboard - Valid Token {i}", "positive", 200, True)
    add_case("/api/dashboard", "GET", "Get Dashboard - No Token", "negative", 401, False)
    for i in range(9):
        add_case("/api/dashboard", "GET", f"Get Dashboard - Unauthorized Probe {i}", "negative", 401, False, headers={"Authorization": f"Bearer token_{i}"})

    # 9. Model Info Scenarios (20 cases)
    for i in range(15):
        add_case("/api/model/info", "GET", f"Get Model Info - Valid Token {i}", "positive", 200, True)
    add_case("/api/model/info", "GET", "Get Model Info - No Token", "negative", 401, False)
    for i in range(4):
        add_case("/api/model/info", "GET", f"Get Model Info - Unauthorized Probe {i}", "negative", 401, False, headers={"Authorization": f"Bearer token_{i}"})

    # 10. Model Retrain Scenarios (20 cases)
    for i in range(15):
        add_case("/api/model/retrain", "POST", f"Force Model Retrain - Valid Token {i}", "positive", 200, True)
    add_case("/api/model/retrain", "POST", "Force Model Retrain - No Token", "negative", 401, False)
    for i in range(4):
        add_case("/api/model/retrain", "POST", f"Force Model Retrain - Unauthorized Probe {i}", "negative", 401, False, headers={"Authorization": f"Bearer token_{i}"})

    # Double-check total
    print(f"Generated {len(scenarios)} unique test scenarios.")
    
    os.makedirs("load-testing", exist_ok=True)
    with open("load-testing/scenarios.json", "w") as f:
        json.dump(scenarios, f, indent=2)
    print("Scenarios saved to load-testing/scenarios.json")

if __name__ == "__main__":
    generate_scenarios()
