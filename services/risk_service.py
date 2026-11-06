import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import os
import functools

# Load model from project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "risk_model.pkl")

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    print(f"ERROR: Model file {MODEL_PATH} not found!")
    model = None

@functools.lru_cache(maxsize=48)
def _predict_risk_for_hour(hour: int) -> float:
    if model is None:
        return 0.5
        
    # features: time, lighting, crowd, crime, weather
    # Lighting: higher in day, lower at night
    lighting = 0.8 if (6 <= hour <= 18) else 0.2
    
    # Crowd: depends on location + time (Simplified for this project)
    crowd = 0.6 if (8 <= hour <= 20) else 0.3
    
    # Crime: constant base risk (0–1)
    crime = 0.1
    
    # Weather: clear (0)
    weather = 0.1
    
    # Create DataFrame with names to match training features
    features_df = pd.DataFrame([{
        "time": hour,
        "lighting": lighting,
        "crowd": crowd,
        "crime": crime,
        "weather": weather
    }])
    
    # Pass DataFrame instead of list to avoid feature name warnings
    risk_prob = model.predict_proba(features_df)[0][1]
    return float(risk_prob)

def get_node_risk(lat, lon):
    if model is None:
        return 0.5  # Default if model not found
        
    current_hour = datetime.now().hour
    return _predict_risk_for_hour(current_hour)
