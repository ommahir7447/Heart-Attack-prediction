import pandas as pd
from utils.model import get_model, load_artifacts


def _build_engineered_input(data: dict) -> pd.DataFrame:
    """Apply the same feature engineering used during training."""
    df = pd.DataFrame(data)

    # Engineered features (must mirror train_model.preprocess)
    df["age_risk"] = pd.cut(
        df["age"], bins=[0, 40, 55, 70, 120], labels=[0, 1, 2, 3]
    ).astype(float)
    df["bp_chol_interaction"] = df["trestbps"] * df["chol"] / 10000.0
    df["hr_reserve"] = df["thalach"] / (220 - df["age"])
    df["st_severe"] = (df["oldpeak"] >= 2.0).astype(int)
    df["age_sex"] = df["age"] * df["sex"]
    df["exercise_risk"] = df["exang"] + (df["oldpeak"] / 4.0) + (df["slope"] / 2.0)

    df = df.fillna(0)
    return df


def test_model_loading():
    model, features = load_artifacts()
    assert model is not None, "Failed to load the model"
    assert features is not None, "Failed to load feature names"


def test_feature_count():
    """Ensure saved feature list matches the expected 19 engineered features."""
    _, features = load_artifacts()
    assert len(features) == 19, f"Expected 19 features, got {len(features)}"


def test_model_prediction_format():
    model = get_model()
    # Dummy raw clinical data
    raw = {
        'age': [50], 'sex': [1], 'cp': [0], 'trestbps': [120], 'chol': [200],
        'fbs': [0], 'restecg': [0], 'thalach': [150], 'exang': [0],
        'oldpeak': [1.0], 'slope': [1], 'ca': [0], 'thal': [2]
    }
    input_df = _build_engineered_input(raw)

    if model is not None:
        prediction_proba = model.predict_proba(input_df)[0][1]
        assert 0.0 <= prediction_proba <= 1.0, "Probability should be between 0 and 1"


def test_model_prediction_class():
    """Prediction class should be 0 or 1."""
    model = get_model()
    raw = {
        'age': [65], 'sex': [1], 'cp': [3], 'trestbps': [160], 'chol': [300],
        'fbs': [1], 'restecg': [2], 'thalach': [100], 'exang': [1],
        'oldpeak': [3.5], 'slope': [2], 'ca': [3], 'thal': [3]
    }
    input_df = _build_engineered_input(raw)

    if model is not None:
        pred_class = model.predict(input_df)[0]
        assert pred_class in (0, 1), f"Expected 0 or 1, got {pred_class}"
