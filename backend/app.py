from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from db import init_db
from auth import auth_bp
from routes import routes_bp

app = Flask(__name__)

# Config
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'neuro-drift-jwt-secret-key-99128')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False # Token never expires for demo ease, or set to standard duration

# Enable CORS for frontend local development server (typically localhost:5173 or localhost:3000)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize JWT Manager
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(routes_bp, url_prefix='/api')

# General Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "An internal server error occurred"}), 500

if __name__ == '__main__':
    # Initialize database on start
    init_db()
    
    # Run server
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Flask backend server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)
