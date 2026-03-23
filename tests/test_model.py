import pytest
import pandas as pd
from utils.model import get_model, load_artifacts

def test_model_loading():
    model, features = load_artifacts()
    assert model is not None, "Failed to load the model"
    assert features is not None, "Failed to load feature names"

def test_model_prediction_format():
    model = get_model()
    # Dummy data
    data = {
        'age': [50], 'sex': [1], 'cp': [0], 'trestbps': [120], 'chol': [200],
        'fbs': [0], 'restecg': [0], 'thalach': [150], 'exang': [0],
        'oldpeak': [1.0], 'slope': [1], 'ca': [0], 'thal': [2]
    }
    input_df = pd.DataFrame(data)
    
    if model is not None:
        prediction_proba = model.predict_proba(input_df)[0][1]
        assert 0.0 <= prediction_proba <= 1.0, "Probability should be between 0 and 1"
