import joblib
import numpy as np
import pandas as pd
import os

# Define healthy baseline for drift calculations
DEFAULT_BASELINE = {
    'screen_time': 180.0,
    'typing_speed': 250.0,
    'typing_error_rate': 0.03,
    'session_duration': 30.0,
    'click_frequency': 30.0,
    'break_frequency': 2.0,
    'mouse_speed': 450.0
}

class CognitiveStrainPredictor:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(base_dir, 'strain_classifier.joblib')
        self.scaler_path = os.path.join(base_dir, 'scaler.joblib')
        
        self.model = None
        self.scaler = None
        self.load_model()
        
    def load_model(self):
        """Lazy load model files."""
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
        else:
            print("Model files not found. Please train the model first.")

    def calculate_drift_score(self, current_metrics, baseline=None):
        """
        Calculate statistical behavioral drift score (0 - 100%)
        comparing current metrics to a baseline profile.
        """
        if baseline is None:
            baseline = DEFAULT_BASELINE
            
        deviations = []
        
        # 1. Typing Speed: lower is worse
        speed_dev = (baseline['typing_speed'] - current_metrics['typing_speed']) / baseline['typing_speed']
        deviations.append(max(0.0, speed_dev))
        
        # 2. Error Rate: higher is worse
        err_dev = (current_metrics['typing_error_rate'] - baseline['typing_error_rate']) / baseline['typing_error_rate']
        # Weight error rate drift heavily
        deviations.append(max(0.0, err_dev) * 1.5)
        
        # 3. Session Duration: higher is worse
        dur_dev = (current_metrics['session_duration'] - baseline['session_duration']) / baseline['session_duration']
        deviations.append(max(0.0, dur_dev))
        
        # 4. Break Frequency: lower is worse
        break_dev = (baseline['break_frequency'] - current_metrics['break_frequency']) / baseline['break_frequency']
        deviations.append(max(0.0, break_dev))
        
        # 5. Mouse Speed: lower (fatigue/sluggishness) is worse
        mouse_dev = (baseline['mouse_speed'] - current_metrics['mouse_speed']) / baseline['mouse_speed']
        deviations.append(max(0.0, mouse_dev))
        
        # Calculate weighted average deviation and convert to percentage
        avg_deviation = sum(deviations) / len(deviations)
        drift_score = min(100.0, avg_deviation * 100.0)
        return round(drift_score, 2)

    def predict_strain(self, metrics):
        """
        Predict cognitive strain level.
        Returns:
            - label: 'Low', 'Medium', or 'High'
            - probability: float confidence
        """
        if self.model is None or self.scaler is None:
            self.load_model()
            if self.model is None or self.scaler is None:
                return 'Low', 1.0 # fallback
                
        # Features ordering must match generate_dataset.py columns:
        # ['screen_time', 'typing_speed', 'typing_error_rate', 'session_duration', 'click_frequency', 'break_frequency', 'mouse_speed']
        features = [
            metrics['screen_time'],
            metrics['typing_speed'],
            metrics['typing_error_rate'],
            metrics['session_duration'],
            metrics['click_frequency'],
            metrics['break_frequency'],
            metrics['mouse_speed']
        ]
        
        features_arr = np.array(features).reshape(1, -1)
        features_scaled = self.scaler.transform(features_arr)
        
        pred_class = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        class_mapping = {0: 'Low', 1: 'Medium', 2: 'High'}
        label = class_mapping.get(pred_class, 'Low')
        probability = float(probabilities[pred_class])
        
        return label, round(probability, 4)
