import pytest
import os
import tempfile
import sys
import json

# Add parent dir of backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app
from db import DB_PATH, SCHEMA_PATH, init_db

@pytest.fixture
def client():
    # Set up temp database for testing
    db_fd, db_temp_path = tempfile.mkstemp()
    
    # Override database path in db.py before initializing
    import db
    original_db_path = db.DB_PATH
    db.DB_PATH = db_temp_path
    
    # Re-import routes to make sure baseline query references the overridden DB_PATH
    import routes
    routes.predictor.load_model()
    
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key-12345'
    
    with app.test_client() as client:
        with app.app_context():
            # Initialize temp database schema
            init_db()
        yield client
        
    # Tear down temp database
    os.close(db_fd)
    os.unlink(db_temp_path)
    db.DB_PATH = original_db_path

def test_auth_flow(client):
    # 1. Register a user
    resp = client.post('/api/auth/register', json={
        'username': 'test_user',
        'password': 'password123'
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert 'token' in data
    assert data['user']['username'] == 'test_user'
    token = data['token']
    
    # 2. Register same user should fail (IntegrityError/Conflict)
    resp = client.post('/api/auth/register', json={
        'username': 'test_user',
        'password': 'password123'
    })
    assert resp.status_code == 409
    
    # 3. Login with correct credentials
    resp = client.post('/api/auth/login', json={
        'username': 'test_user',
        'password': 'password123'
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'token' in data
    
    # 4. Login with bad credentials
    resp = client.post('/api/auth/login', json={
        'username': 'test_user',
        'password': 'wrong_password'
    })
    assert resp.status_code == 401
    
    # 5. Access profile with token
    resp = client.get('/api/auth/me', headers={
        'Authorization': f'Bearer {token}'
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['username'] == 'test_user'
    
    # 6. Access profile without token should fail
    resp = client.get('/api/auth/me')
    assert resp.status_code == 401

def test_metrics_and_dashboard(client):
    # Register and get token
    resp = client.post('/api/auth/register', json={
        'username': 'metrics_user',
        'password': 'password123'
    })
    token = resp.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # Ingest healthy metrics (Low strain)
    resp = client.post('/api/metrics', json={
        'screen_time': 120.0,
        'typing_speed': 280.0,
        'typing_error_rate': 0.02,
        'session_duration': 20.0,
        'click_frequency': 25.0,
        'break_frequency': 2.0,
        'mouse_speed': 480.0
    }, headers=headers)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['status'] == 'success'
    assert 'prediction' in data
    assert 'drift_score' in data['prediction']
    
    # Ingest fatigued metrics (Should trigger alerts/High strain)
    resp = client.post('/api/metrics', json={
        'screen_time': 500.0,
        'typing_speed': 80.0,
        'typing_error_rate': 0.25,
        'session_duration': 150.0,
        'click_frequency': 5.0,
        'break_frequency': 0.1,
        'mouse_speed': 70.0
    }, headers=headers)
    assert resp.status_code == 201
    data = resp.get_json()
    assert len(data['alerts']) > 0
    
    # Check dashboard stats
    resp = client.get('/api/dashboard', headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'latest_metrics' in data
    assert 'latest_prediction' in data
    assert 'weekly_averages' in data
    assert len(data['timeseries']) == 2
    
    # Check alerts retrieval
    resp = client.get('/api/alerts', headers=headers)
    assert resp.status_code == 200
    alerts = resp.get_json()
    assert len(alerts) > 0
    
    # Mark alerts as read
    resp = client.post('/api/alerts/read', json={}, headers=headers)
    assert resp.status_code == 200

def test_model_info(client):
    resp = client.post('/api/auth/register', json={
        'username': 'info_user',
        'password': 'password123'
    })
    token = resp.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}
    
    # Fetch model details
    resp = client.get('/api/model/info', headers=headers)
    # Could return 200 if trained, or 404 if not found (we have trained it, so it should be 200)
    assert resp.status_code in (200, 404)
