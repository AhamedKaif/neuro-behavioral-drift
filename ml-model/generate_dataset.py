import pandas as pd
import numpy as np
import os

def generate_synthetic_data(num_samples=1200):
    np.random.seed(42)
    
    # Target distribution: 1/3 Low, 1/3 Medium, 1/3 High
    samples_per_class = num_samples // 3
    
    data = []
    
    # Class 0: Low Cognitive Strain (Healthy, productive baseline)
    for _ in range(samples_per_class):
        screen_time = np.random.uniform(60, 240) # minutes/day
        typing_speed = np.random.uniform(200, 350) # CPM
        typing_error_rate = np.random.uniform(0.01, 0.05) # ratio
        session_duration = np.random.uniform(10, 45) # continuous minutes
        click_frequency = np.random.uniform(15, 45) # clicks/min
        break_frequency = np.random.uniform(1.5, 3.5) # breaks/hour
        mouse_speed = np.random.uniform(300, 600) # px/sec
        
        data.append({
            'screen_time': screen_time,
            'typing_speed': typing_speed,
            'typing_error_rate': typing_error_rate,
            'session_duration': session_duration,
            'click_frequency': click_frequency,
            'break_frequency': break_frequency,
            'mouse_speed': mouse_speed,
            'cognitive_strain': 0 # Low
        })
        
    # Class 1: Medium Cognitive Strain (Moderate fatigue/prolonged work)
    for _ in range(samples_per_class):
        screen_time = np.random.uniform(240, 480)
        typing_speed = np.random.uniform(140, 210)
        typing_error_rate = np.random.uniform(0.05, 0.12)
        session_duration = np.random.uniform(45, 90)
        click_frequency = np.random.uniform(10, 25)
        break_frequency = np.random.uniform(0.5, 1.5)
        mouse_speed = np.random.uniform(150, 350)
        
        data.append({
            'screen_time': screen_time,
            'typing_speed': typing_speed,
            'typing_error_rate': typing_error_rate,
            'session_duration': session_duration,
            'click_frequency': click_frequency,
            'break_frequency': break_frequency,
            'mouse_speed': mouse_speed,
            'cognitive_strain': 1 # Medium
        })
        
    # Class 2: High Cognitive Strain (Severe exhaustion, heavy behavioral drift)
    for _ in range(samples_per_class):
        screen_time = np.random.uniform(480, 720)
        typing_speed = np.random.uniform(70, 140)
        typing_error_rate = np.random.uniform(0.12, 0.28)
        session_duration = np.random.uniform(90, 180)
        click_frequency = np.random.uniform(4, 15)
        break_frequency = np.random.uniform(0.0, 0.5)
        mouse_speed = np.random.uniform(50, 180)
        
        data.append({
            'screen_time': screen_time,
            'typing_speed': typing_speed,
            'typing_error_rate': typing_error_rate,
            'session_duration': session_duration,
            'click_frequency': click_frequency,
            'break_frequency': break_frequency,
            'mouse_speed': mouse_speed,
            'cognitive_strain': 2 # High
        })
        
    df = pd.DataFrame(data)
    # Shuffle dataset
    df = df.sample(frac=1).reset_index(drop=True)
    
    # Save file
    output_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, 'behavioral_drift_dataset.csv')
    df.to_csv(output_path, index=False)
    print(f"Synthetic dataset saved to {output_path} with {len(df)} samples.")

if __name__ == '__main__':
    generate_synthetic_data()
