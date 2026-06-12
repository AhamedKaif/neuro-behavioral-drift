from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from db import init_db
from auth import auth_bp
from routes import routes_bp
from user_profile import user_profile_bp
from notifications import notifications_bp

frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist'))
app = Flask(__name__, static_folder=frontend_dist, static_url_path='/')

# Config
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'neuro-drift-jwt-secret-key-99128')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30) # Token valid for 30 days

# Enable CORS for frontend local development server (typically localhost:5173 or localhost:3000)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize JWT Manager
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_profile_bp, url_prefix='/api/profile')
app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
app.register_blueprint(routes_bp, url_prefix='/api')

# General Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "An internal server error occurred"}), 500

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Only serve the index.html if the path does not match a file in the static folder
    # This prevents the frontend from intercepting API routes (since they start with /api and are registered above)
    # and allows React Router to handle frontend routes.
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return app.send_static_file(path)
    else:
        return app.send_static_file('index.html')


if __name__ == '__main__':
    # Initialize database on start
    init_db()
    
    # Run server
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Flask backend server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)
