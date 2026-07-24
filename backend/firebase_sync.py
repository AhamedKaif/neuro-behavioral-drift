import urllib.request
import json
import ssl
from db import get_db_connection

import os

FIREBASE_URL = os.environ.get("FIREBASE_DATABASE_URL", "https://neurobehavior-drift-prod-default-rtdb.firebaseio.com")
if FIREBASE_URL.endswith('/'):
    FIREBASE_URL = FIREBASE_URL[:-1]
ssl_context = ssl._create_unverified_context()

def sync_to_firebase(username, user_data, profile_data=None):
    try:
        # 1. Sync User credentials
        url = f"{FIREBASE_URL}/users/{username}.json"
        req = urllib.request.Request(
            url,
            data=json.dumps(user_data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='PUT'
        )
        with urllib.request.urlopen(req, context=ssl_context) as response:
            response.read()

        # 2. Sync Profile
        if profile_data:
            url_profile = f"{FIREBASE_URL}/profiles/{username}.json"
            req_p = urllib.request.Request(
                url_profile,
                data=json.dumps(profile_data).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='PUT'
            )
            with urllib.request.urlopen(req_p, context=ssl_context) as response:
                response.read()
    except Exception as e:
        print(f"Error syncing to Firebase: {e}")

def sync_from_firebase(username):
    try:
        # Check if user exists in Firebase
        url = f"{FIREBASE_URL}/users/{username}.json"
        req = urllib.request.Request(url, method='GET')
        with urllib.request.urlopen(req, context=ssl_context) as response:
            raw_res = response.read()
            user_data = json.loads(raw_res.decode('utf-8'))
        
        if not user_data:
            return False

        # Get profile data
        url_profile = f"{FIREBASE_URL}/profiles/{username}.json"
        req_p = urllib.request.Request(url_profile, method='GET')
        with urllib.request.urlopen(req_p, context=ssl_context) as response:
            profile_data = json.loads(response.read().decode('utf-8')) or {}

        # Get password hash or generate it from plaintext password if synced from mobile
        password_hash = user_data.get('password_hash')
        if not password_hash and user_data.get('password'):
            from werkzeug.security import generate_password_hash
            password_hash = generate_password_hash(user_data.get('password'))

        # Fetch full name from profile data if not present in credentials object
        full_name = user_data.get('full_name') or profile_data.get('fullName') or profile_data.get('full_name') or 'User'

        # Insert into local SQLite db
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (full_name, username, email, password_hash) VALUES (?, ?, ?, ?)",
            (full_name, username, user_data.get('email'), password_hash)
        )
        user_id = cursor.lastrowid

        cursor.execute(
            """INSERT INTO user_profiles (
                user_id, age, gender, occupation, institution, department, academic_year,
                working_hours, avg_screen_time, avg_sleep_hours, preferred_work_time, stress_level
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user_id,
                profile_data.get('age'),
                profile_data.get('gender'),
                profile_data.get('occupation'),
                profile_data.get('institution'),
                profile_data.get('department'),
                profile_data.get('academic_year'),
                profile_data.get('working_hours'),
                profile_data.get('avg_screen_time'),
                profile_data.get('avg_sleep_hours'),
                profile_data.get('preferred_work_time'),
                profile_data.get('stress_level')
            )
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error syncing from Firebase: {e}")
        return False

def sync_profile_from_firebase(username):
    try:
        url_profile = f"{FIREBASE_URL}/profiles/{username}.json"
        req_p = urllib.request.Request(url_profile, method='GET')
        with urllib.request.urlopen(req_p, context=ssl_context) as response:
            profile_data = json.loads(response.read().decode('utf-8')) or {}
        
        if not profile_data:
            return False

        url = f"{FIREBASE_URL}/users/{username}.json"
        req = urllib.request.Request(url, method='GET')
        with urllib.request.urlopen(req, context=ssl_context) as response:
            user_data = json.loads(response.read().decode('utf-8')) or {}

        full_name = user_data.get('full_name') or profile_data.get('fullName') or profile_data.get('full_name') or 'User'

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET full_name = ? WHERE username = ?", (full_name, username))
        user_row = cursor.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        
        if user_row:
            user_id = user_row['id']
            cursor.execute(
                """UPDATE user_profiles SET 
                    age = ?, gender = ?, occupation = ?, institution = ?, department = ?, academic_year = ?,
                    working_hours = ?, avg_screen_time = ?, avg_sleep_hours = ?, preferred_work_time = ?, stress_level = ?
                   WHERE user_id = ?""",
                (
                    profile_data.get('age'),
                    profile_data.get('gender'),
                    profile_data.get('occupation'),
                    profile_data.get('institution'),
                    profile_data.get('department'),
                    profile_data.get('academic_year'),
                    profile_data.get('working_hours'),
                    profile_data.get('avg_screen_time'),
                    profile_data.get('avg_sleep_hours'),
                    profile_data.get('preferred_work_time'),
                    profile_data.get('stress_level'),
                    user_id
                )
            )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error syncing profile from Firebase: {e}")
        return False
