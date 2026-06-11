-- SQL Database Schema for Neuro-Behavioral Drift Monitoring System
-- Compatible with SQLite (development) and PostgreSQL (production)

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Behavioral Metrics Table (Time-series data points)
CREATE TABLE IF NOT EXISTS behavioral_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    screen_time REAL NOT NULL, -- Total active screen time (minutes) in the current day
    typing_speed REAL NOT NULL, -- Keystrokes per minute (CPM)
    typing_error_rate REAL NOT NULL, -- Ratio of Backspaces/Delete keys to total keystrokes
    session_duration REAL NOT NULL, -- Active session length (minutes)
    click_frequency REAL NOT NULL, -- Clicks per minute
    break_frequency REAL NOT NULL, -- Breaks taken per hour
    mouse_speed REAL NOT NULL, -- Average mouse speed in pixels/second
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Indexing for optimized historical queries
CREATE INDEX IF NOT EXISTS idx_metrics_user_time ON behavioral_metrics (user_id, timestamp);

-- 3. Predictions Table (Cognitive Strain & Drift Scores)
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    drift_score REAL NOT NULL, -- Deviation from user's personal baseline (0.0 to 100.0)
    strain_label VARCHAR(20) NOT NULL, -- 'Low', 'Medium', 'High'
    strain_probability REAL NOT NULL, -- Probability confidence (0.0 to 1.0)
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_predictions_user_time ON predictions (user_id, timestamp);

-- 4. System Alerts Table (Reminders and Strain Warnings)
CREATE TABLE IF NOT EXISTS system_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    alert_type VARCHAR(50) NOT NULL, -- 'HIGH_STRAIN', 'LONG_SESSION', 'BREAK_REMINDER'
    message TEXT NOT NULL,
    is_read INTEGER DEFAULT 0, -- 0 = False, 1 = True (SQLite boolean representation)
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_alerts_user_time ON system_alerts (user_id, timestamp);
