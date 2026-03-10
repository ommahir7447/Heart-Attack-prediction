import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import joblib
import matplotlib.pyplot as plt
import os

# Set page config
st.set_page_config(page_title="Heart Attack Risk Predictor", layout="wide")

# Load model and features
@st.cache_resource
def load_artifacts():
    model = joblib.load("models/heart_attack_model.joblib")
    features = joblib.load("models/feature_names.joblib")
    return model, features

try:
    model, feature_names = load_artifacts()
except Exception as e:
    st.error(f"Error loading model: {e}. Please run train_model.py first.")
    st.stop()

# Sidebar for inputs
st.sidebar.header("User Clinical Data")

def get_user_input():
    age = st.sidebar.slider("Age", 20, 90, 50)
    sex = st.sidebar.selectbox("Sex", options=[0, 1], format_func=lambda x: "Male" if x == 1 else "Female")
    cp = st.sidebar.selectbox("Chest Pain Type (0-3)", options=[0, 1, 2, 3])
    trestbps = st.sidebar.slider("Resting Blood Pressure", 80, 200, 120)
    chol = st.sidebar.slider("Serum Cholestoral (mg/dl)", 100, 600, 200)
    fbs = st.sidebar.selectbox("Fasting Blood Sugar > 120 mg/dl", options=[0, 1])
    restecg = st.sidebar.selectbox("Resting Electrocardiographic Results (0-2)", options=[0, 1, 2])
    thalach = st.sidebar.slider("Maximum Heart Rate Achieved", 60, 220, 150)
    exang = st.sidebar.selectbox("Exercise Induced Angina", options=[0, 1])
    oldpeak = st.sidebar.slider("ST depression induced by exercise", 0.0, 7.0, 1.0)
    slope = st.sidebar.selectbox("Slope of the peak exercise ST segment (0-2)", options=[0, 1, 2])
    ca = st.sidebar.selectbox("Number of major vessels (0-3)", options=[0, 1, 2, 3])
    thal = st.sidebar.selectbox("Thal (1 = normal; 2 = fixed defect; 3 = reversable defect)", options=[1, 2, 3])

    data = {
        'age': age, 'sex': sex, 'cp': cp, 'trestbps': trestbps, 'chol': chol,
        'fbs': fbs, 'restecg': restecg, 'thalach': thalach, 'exang': exang,
        'oldpeak': oldpeak, 'slope': slope, 'ca': ca, 'thal': thal
    }
    return pd.DataFrame(data, index=[0])

input_df = get_user_input()

# Main page
st.title("Explainable Heart Attack Risk Prediction")
st.markdown("""
This app predicts the likelihood of a heart attack based on clinical factors and provides an explanation using SHAP values.
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Prediction Results")
    prediction_proba = model.predict_proba(input_df)[0][1]
    prediction = 1 if prediction_proba > 0.5 else 0
    
    risk_level = "High" if prediction == 1 else "Low"
    st.metric("Heart Attack Risk", risk_level, f"{prediction_proba:.2%}")
    
    if prediction == 1:
        st.warning("⚠️ High Risk Detected: Consultation with a healthcare professional is recommended.")
    else:
        st.success("✅ Low Risk Detected: Maintain a healthy lifestyle.")

with col2:
    st.subheader("Clinical Factors Summary")
    st.write(input_df)

st.divider()

# Explainability Section
st.header("🔍 Why this prediction?")
st.markdown("SHAP (SHapley Additive exPlanations) values break down the contribution of each clinical factor to the final risk score.")

try:
    # Initialize SHAP explainer
    explainer = shap.Explainer(model)
    shap_values = explainer(input_df)

    # Visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    shap.plots.waterfall(shap_values[0], show=False)
    st.pyplot(plt.gcf())
    
    st.info("""
    **How to read this plot:**
    - **Positive (red)** values increase the risk probability.
    - **Negative (blue)** values decrease the risk probability.
    - The **f(x)** is the predicted log-odds, which we convert to probability above.
    """)
    
except Exception as e:
    st.error(f"Error generating SHAP explanation: {e}")

st.divider()
st.markdown("Built with Python, XGBoost, SHAP, and Streamlit.")
