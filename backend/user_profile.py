from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db_connection

user_profile_bp = Blueprint('profile', __name__)

@user_profile_bp.route('', methods=['GET'], strict_slashes=False)
@user_profile_bp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    
    # Get user basics
    user = conn.execute(
        "SELECT id, full_name, username, email, created_at FROM users WHERE id = ?", 
        (user_id,)
    ).fetchone()
    
    if not user:
        conn.close()
        return jsonify({"error": "User not found"}), 404
        
    # Get profile details
    profile = conn.execute(
        "SELECT * FROM user_profiles WHERE user_id = ?", 
        (user_id,)
    ).fetchone()
    
    # Get analytics summary (latest prediction)
    latest_pred = conn.execute(
        "SELECT drift_score, strain_label, timestamp FROM predictions WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1",
        (user_id,)
    ).fetchone()
    
    conn.close()
    
    profile_data = dict(profile) if profile else {}
    if 'id' in profile_data:
        del profile_data['id']
    if 'user_id' in profile_data:
        del profile_data['user_id']
        
    return jsonify({
        "account": {
            "id": user['id'],
            "full_name": user['full_name'],
            "username": user['username'],
            "email": user['email'],
            "created_at": user['created_at']
        },
        "profile": profile_data,
        "analytics": {
            "drift_score": latest_pred['drift_score'] if latest_pred else None,
            "strain_label": latest_pred['strain_label'] if latest_pred else None,
            "last_prediction": latest_pred['timestamp'] if latest_pred else None
        }
    }), 200

@user_profile_bp.route('', methods=['PUT'], strict_slashes=False)
@user_profile_bp.route('/', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    # Type & Boundary validations
    if 'age' in data:
        age = data.get('age')
        if age is not None:
            try:
                age = int(age)
                if age < 0 or age > 120:
                    return jsonify({"error": "Age must be between 0 and 120"}), 400
                data['age'] = age
            except (ValueError, TypeError):
                return jsonify({"error": "Age must be an integer"}), 400

    if 'stress_level' in data:
        stress_level = data.get('stress_level')
        if stress_level is not None:
            try:
                stress_level = int(stress_level)
                if stress_level < 1 or stress_level > 10:
                    return jsonify({"error": "Stress level must be between 1 and 10"}), 400
                data['stress_level'] = stress_level
            except (ValueError, TypeError):
                return jsonify({"error": "Stress level must be an integer"}), 400

    if 'working_hours' in data:
        working_hours = data.get('working_hours')
        if working_hours is not None:
            try:
                working_hours = float(working_hours)
                data['working_hours'] = working_hours
            except (ValueError, TypeError):
                return jsonify({"error": "Working hours must be numeric"}), 400

    if 'avg_screen_time' in data:
        avg_screen_time = data.get('avg_screen_time')
        if avg_screen_time is not None:
            try:
                avg_screen_time = float(avg_screen_time)
                data['avg_screen_time'] = avg_screen_time
            except (ValueError, TypeError):
                return jsonify({"error": "Average screen time must be numeric"}), 400

    if 'avg_sleep_hours' in data:
        avg_sleep_hours = data.get('avg_sleep_hours')
        if avg_sleep_hours is not None:
            try:
                avg_sleep_hours = float(avg_sleep_hours)
                data['avg_sleep_hours'] = avg_sleep_hours
            except (ValueError, TypeError):
                return jsonify({"error": "Average sleep hours must be numeric"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Update full name if provided
        if 'full_name' in data:
            cursor.execute("UPDATE users SET full_name = ? WHERE id = ?", (data['full_name'], user_id))
            
        # Update profile fields
        update_fields = [
            'age', 'gender', 'occupation', 'institution', 'department', 
            'academic_year', 'working_hours', 'avg_screen_time', 
            'avg_sleep_hours', 'preferred_work_time', 'stress_level'
        ]
        
        updates = []
        values = []
        for field in update_fields:
            if field in data:
                updates.append(f"{field} = ?")
                values.append(data[field])
                
        if updates:
            values.append(user_id)
            query = f"UPDATE user_profiles SET {', '.join(updates)} WHERE user_id = ?"
            cursor.execute(query, values)
            
        conn.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@user_profile_bp.route('/account', methods=['DELETE'])
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    
    try:
        # Due to ON DELETE CASCADE in schema.sql, deleting the user will delete profile, metrics, predictions, and alerts.
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return jsonify({"message": "Account deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
