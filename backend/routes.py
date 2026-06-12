import sys
import os
import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db_connection

# Add ml-model to python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ml-model'))
from predictor import CognitiveStrainPredictor, DEFAULT_BASELINE
from train import train_model

routes_bp = Blueprint('routes', __name__)
predictor = CognitiveStrainPredictor()

def get_user_baseline(user_id):
    """
    Retrieve user baseline from database.
    Baseline is defined as the average metrics when strain was 'Low'.
    If not enough data (e.g. < 5 records), fall back to DEFAULT_BASELINE.
    """
    conn = get_db_connection()
    # Select averages where prediction was Low
    query = """
        SELECT 
            AVG(m.screen_time) as screen_time,
            AVG(m.typing_speed) as typing_speed,
            AVG(m.typing_error_rate) as typing_error_rate,
            AVG(m.session_duration) as session_duration,
            AVG(m.click_frequency) as click_frequency,
            AVG(m.break_frequency) as break_frequency,
            AVG(m.mouse_speed) as mouse_speed
        FROM behavioral_metrics m
        JOIN predictions p ON m.user_id = p.user_id AND m.id = p.id
        WHERE m.user_id = ? AND p.strain_label = 'Low'
    """
    row = conn.execute(query, (user_id,)).fetchone()
    conn.close()
    
    if row and row['screen_time'] is not None:
        return {
            'screen_time': row['screen_time'],
            'typing_speed': row['typing_speed'],
            'typing_error_rate': row['typing_error_rate'],
            'session_duration': row['session_duration'],
            'click_frequency': row['click_frequency'],
            'break_frequency': row['break_frequency'],
            'mouse_speed': row['mouse_speed']
        }
    return DEFAULT_BASELINE

@routes_bp.route('/metrics', methods=['POST'])
@jwt_required()
def ingest_metrics():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    # Required keys
    required_keys = ['screen_time', 'typing_speed', 'typing_error_rate', 'session_duration', 
                     'click_frequency', 'break_frequency', 'mouse_speed']
    
    missing = [k for k in required_keys if k not in data]
    if missing:
        return jsonify({"error": f"Missing parameters: {', '.join(missing)}"}), 400
        
    try:
        metrics = {k: float(data[k]) for k in required_keys}
    except ValueError:
        return jsonify({"error": "All metric values must be numeric"}), 400
        
    # Get user baseline and run prediction
    baseline = get_user_baseline(user_id)
    drift_score = predictor.calculate_drift_score(metrics, baseline)
    strain_label, probability = predictor.predict_strain(metrics)
    
    # Insert metrics and predictions into database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO behavioral_metrics (user_id, screen_time, typing_speed, typing_error_rate, 
                                        session_duration, click_frequency, break_frequency, mouse_speed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, metrics['screen_time'], metrics['typing_speed'], metrics['typing_error_rate'],
          metrics['session_duration'], metrics['click_frequency'], metrics['break_frequency'], metrics['mouse_speed']))
          
    cursor.execute("""
        INSERT INTO predictions (user_id, drift_score, strain_label, strain_probability)
        VALUES (?, ?, ?, ?)
    """, (user_id, drift_score, strain_label, probability))
    
    # Create notifications if conditions are met
    alerts = []
    
    # Alert 1: High Strain
    if strain_label == 'High':
        alert_msg = "High cognitive strain detected based on your interaction patterns. We highly recommend taking a 15-minute screen break."
        cursor.execute(
            "INSERT INTO system_alerts (user_id, alert_type, message) VALUES (?, ?, ?)",
            (user_id, 'HIGH_STRAIN', alert_msg)
        )
        alerts.append({"type": "HIGH_STRAIN", "message": alert_msg})
        
    # Alert 2: Long continuous session
    if metrics['session_duration'] >= 90.0:
        alert_msg = f"Continuous session has reached {int(metrics['session_duration'])} minutes. Take a step back to prevent eye strain."
        cursor.execute(
            "INSERT INTO system_alerts (user_id, alert_type, message) VALUES (?, ?, ?)",
            (user_id, 'LONG_SESSION', alert_msg)
        )
        alerts.append({"type": "LONG_SESSION", "message": alert_msg})
        
    # Alert 3: Lack of breaks
    if metrics['break_frequency'] < 0.5 and metrics['session_duration'] >= 60.0:
        alert_msg = "You are taking fewer breaks than recommended. Keep hydrated and stand up for a stretch."
        cursor.execute(
            "INSERT INTO system_alerts (user_id, alert_type, message) VALUES (?, ?, ?)",
            (user_id, 'BREAK_REMINDER', alert_msg)
        )
        alerts.append({"type": "BREAK_REMINDER", "message": alert_msg})
        
    conn.commit()
    conn.close()
    
    return jsonify({
        "status": "success",
        "prediction": {
            "strain_label": strain_label,
            "probability": probability,
            "drift_score": drift_score
        },
        "alerts": alerts
    }), 201

@routes_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_data():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    
    # 1. Latest metrics
    latest_metrics_row = conn.execute("""
        SELECT * FROM behavioral_metrics 
        WHERE user_id = ? 
        ORDER BY timestamp DESC LIMIT 1
    """, (user_id,)).fetchone()
    
    # 2. Latest prediction
    latest_pred_row = conn.execute("""
        SELECT * FROM predictions 
        WHERE user_id = ? 
        ORDER BY timestamp DESC LIMIT 1
    """, (user_id,)).fetchone()
    
    from datetime import datetime, timedelta
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    # 3. Weekly averages
    weekly_avg_row = conn.execute("""
        SELECT 
            AVG(screen_time) as avg_screen_time,
            AVG(session_duration) as avg_session_duration,
            AVG(typing_speed) as avg_typing_speed,
            AVG(typing_error_rate) as avg_error_rate,
            AVG(break_frequency) as avg_break_frequency
        FROM behavioral_metrics
        WHERE user_id = ? AND timestamp >= ?
    """, (user_id, seven_days_ago)).fetchone()
    
    # 4. Timeseries data (Last 7 days of logs)
    timeseries_rows = conn.execute("""
        SELECT 
            strftime('%Y-%m-%d %H:%M', m.timestamp) as time_label,
            m.screen_time,
            m.typing_speed,
            m.session_duration,
            m.typing_error_rate,
            p.drift_score,
            p.strain_label
        FROM behavioral_metrics m
        LEFT JOIN predictions p ON m.user_id = p.user_id AND m.id = p.id
        WHERE m.user_id = ? 
        ORDER BY m.timestamp DESC LIMIT 15
    """, (user_id,)).fetchall()
    
    conn.close()
    
    # Map row data to dicts
    latest_metrics = dict(latest_metrics_row) if latest_metrics_row else None
    latest_pred = dict(latest_pred_row) if latest_pred_row else None
    
    weekly_averages = {
        "screen_time": round(weekly_avg_row['avg_screen_time'], 1) if weekly_avg_row and weekly_avg_row['avg_screen_time'] else 0.0,
        "session_duration": round(weekly_avg_row['avg_session_duration'], 1) if weekly_avg_row and weekly_avg_row['avg_session_duration'] else 0.0,
        "typing_speed": round(weekly_avg_row['avg_typing_speed'], 1) if weekly_avg_row and weekly_avg_row['avg_typing_speed'] else 0.0,
        "typing_error_rate": round(weekly_avg_row['avg_error_rate'], 3) if weekly_avg_row and weekly_avg_row['avg_error_rate'] else 0.0,
        "break_frequency": round(weekly_avg_row['avg_break_frequency'], 2) if weekly_avg_row and weekly_avg_row['avg_break_frequency'] else 0.0,
    }
    
    # Reverse to chronological order for charts
    timeseries = []
    for r in reversed(timeseries_rows):
        timeseries.append(dict(r))
        
    # User baseline for radar chart
    baseline = get_user_baseline(user_id)
    
    return jsonify({
        "latest_metrics": latest_metrics,
        "latest_prediction": latest_pred,
        "weekly_averages": weekly_averages,
        "timeseries": timeseries,
        "baseline": baseline
    }), 200

@routes_bp.route('/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    alerts = conn.execute("""
        SELECT * FROM system_alerts 
        WHERE user_id = ? 
        ORDER BY timestamp DESC LIMIT 20
    """, (user_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(a) for a in alerts]), 200

@routes_bp.route('/alerts/read', methods=['POST'])
@jwt_required()
def mark_alerts_read():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    alert_id = data.get('alert_id')
    
    conn = get_db_connection()
    if alert_id:
        conn.execute("UPDATE system_alerts SET is_read = 1 WHERE user_id = ? AND id = ?", (user_id, alert_id))
    else:
        conn.execute("UPDATE system_alerts SET is_read = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "Alerts marked as read"}), 200

@routes_bp.route('/model/info', methods=['GET'])
@jwt_required()
def get_model_info():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    metrics_path = os.path.join(base_dir, 'ml-model', 'model_evaluation.json')
    
    if os.path.exists(metrics_path):
        with open(metrics_path, 'r') as f:
            info = json.load(f)
        return jsonify(info), 200
    return jsonify({"error": "Model training evaluation file not found. Please train model."}), 404

@routes_bp.route('/model/retrain', methods=['POST'])
@jwt_required()
def force_retrain():
    try:
        train_model()
        # Reload model inside predictor
        predictor.load_model()
        return jsonify({"status": "success", "message": "Model retrained and reloaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to train model: {str(e)}"}), 500
