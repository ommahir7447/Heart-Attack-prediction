import streamlit as st
import joblib

@st.cache_resource
def load_artifacts():
    try:
        model = joblib.load("models/heart_attack_model.joblib")
        features = joblib.load("models/feature_names.joblib")
        return model, features
    except Exception as e:
        return None, None

def get_model():
    model, _ = load_artifacts()
    return model
