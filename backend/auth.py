from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from db import get_db_connection
import sqlite3

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    full_name = data.get('full_name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Profile fields
    age = data.get('age')
    gender = data.get('gender')
    occupation = data.get('occupation')
    institution = data.get('institution')
    department = data.get('department')
    academic_year = data.get('academic_year')
    working_hours = data.get('working_hours')
    avg_screen_time = data.get('avg_screen_time')
    avg_sleep_hours = data.get('avg_sleep_hours')
    preferred_work_time = data.get('preferred_work_time')
    stress_level = data.get('stress_level')
    
    if not username or not password or not email or not full_name:
        return jsonify({"error": "Full name, username, email, and password are required"}), 400
        
    password_hash = generate_password_hash(password)
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (full_name, username, email, password_hash) VALUES (?, ?, ?, ?)",
            (full_name, username, email, password_hash)
        )
        user_id = cursor.lastrowid
        
        cursor.execute(
            """INSERT INTO user_profiles 
               (user_id, age, gender, occupation, institution, department, academic_year, 
               working_hours, avg_screen_time, avg_sleep_hours, preferred_work_time, stress_level)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, age, gender, occupation, institution, department, academic_year,
             working_hours, avg_screen_time, avg_sleep_hours, preferred_work_time, stress_level)
        )
        conn.commit()
        
        # Auto-login after registration by creating access token
        access_token = create_access_token(identity=str(user_id))
        return jsonify({
            "message": "User registered successfully",
            "token": access_token,
            "user": {"id": user_id, "username": username, "email": email, "full_name": full_name}
        }), 201
    except sqlite3.IntegrityError as e:
        if 'email' in str(e).lower():
            return jsonify({"error": "Email already exists"}), 409
        return jsonify({"error": "Username already exists"}), 409
    finally:
        conn.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
        
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    
    if user is None or not check_password_hash(user['password_hash'], password):
        return jsonify({"error": "Invalid username or password"}), 401
        
    access_token = create_access_token(identity=str(user['id']))
    return jsonify({
        "message": "Login successful",
        "token": access_token,
        "user": {
            "id": user['id'], 
            "username": user['username'],
            "email": user['email'],
            "full_name": user['full_name']
        }
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    user = conn.execute("SELECT id, full_name, username, email, created_at FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    return jsonify({
        "id": user['id'],
        "full_name": user['full_name'],
        "username": user['username'],
        "email": user['email'],
        "created_at": user['created_at']
    }), 200
