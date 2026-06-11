import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import json
import os

def train_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, 'behavioral_drift_dataset.csv')
    
    # Check if dataset exists, if not generate it
    if not os.path.exists(dataset_path):
        print("Dataset not found. Generating dataset first...")
        from generate_dataset import generate_synthetic_data
        generate_synthetic_data()
        
    df = pd.read_csv(dataset_path)
    
    # Separate features and target
    X = df.drop('cognitive_strain', axis=1)
    y = df['cognitive_strain']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest Classifier
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Predictions and evaluation
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred).tolist()
    report = classification_report(y_test, y_pred, output_dict=True)
    
    print(f"Model Accuracy: {accuracy:.4f}")
    
    # Save Model, Scaler, and Metrics
    model_path = os.path.join(base_dir, 'strain_classifier.joblib')
    scaler_path = os.path.join(base_dir, 'scaler.joblib')
    metrics_path = os.path.join(base_dir, 'model_evaluation.json')
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    
    feature_importance = dict(zip(X.columns, model.feature_importances_.tolist()))
    
    evaluation_results = {
        'accuracy': accuracy,
        'confusion_matrix': conf_matrix,
        'classification_report': report,
        'feature_importance': feature_importance
    }
    
    with open(metrics_path, 'w') as f:
        json.dump(evaluation_results, f, indent=4)
        
    print(f"Model and scaler saved successfully to {base_dir}")
    print("Feature Importances:")
    for feat, imp in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {feat}: {imp:.4f}")

if __name__ == '__main__':
    train_model()
