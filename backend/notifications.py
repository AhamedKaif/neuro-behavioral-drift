from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db_connection

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('', methods=['GET'], strict_slashes=False)
@notifications_bp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()
    severity = request.args.get('severity')
    
    conn = get_db_connection()
    if severity and severity != 'ALL':
        notifications = conn.execute("""
            SELECT * FROM notifications 
            WHERE user_id = ? AND severity = ?
            ORDER BY created_at DESC LIMIT 50
        """, (user_id, severity)).fetchall()
    else:
        notifications = conn.execute("""
            SELECT * FROM notifications 
            WHERE user_id = ? 
            ORDER BY created_at DESC LIMIT 50
        """, (user_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(n) for n in notifications]), 200

@notifications_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    count = conn.execute("""
        SELECT COUNT(*) as cnt FROM notifications 
        WHERE user_id = ? AND is_read = 0
    """, (user_id,)).fetchone()
    conn.close()
    
    return jsonify({"unread_count": count['cnt'] if count else 0}), 200

@notifications_bp.route('/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_read(notification_id):
    user_id = get_jwt_identity()
    conn = get_db_connection()
    conn.execute("UPDATE notifications SET is_read = 1 WHERE id = ? AND user_id = ?", (notification_id, user_id))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 200

@notifications_bp.route('/read-all', methods=['POST'])
@jwt_required()
def mark_all_read():
    user_id = get_jwt_identity()
    conn = get_db_connection()
    conn.execute("UPDATE notifications SET is_read = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 200

@notifications_bp.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    user_id = get_jwt_identity()
    conn = get_db_connection()
    conn.execute("DELETE FROM notifications WHERE id = ? AND user_id = ?", (notification_id, user_id))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 200
