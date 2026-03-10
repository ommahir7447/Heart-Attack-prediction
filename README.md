# Explainable Heart Attack Risk Prediction System

This project implements a machine learning system to predict heart attack risk using clinical data from the UCI Heart Disease (Cleveland) dataset. It utilizes **XGBoost** for classification and **SHAP** for model explainability, all deployed within a **Streamlit** web interface.

## 🚀 Features
- **Accurate Prediction**: Uses XGBoost trained on clinical factors (age, cholesterol, blood pressure, etc.).
- **Explainability**: Integrated SHAP Waterfall plots to show *why* a prediction was made.
- **Real-time Interface**: Interactive Streamlit UI for data input and visualization.
- **Clinical Factors**: Covers 13 key risk factors including CP type, Thalach, and CA.

## 🛠️ Tech Stack
- **Language**: Python
- **ML Model**: XGBoost
- **Explainability**: SHAP (SHapley Additive exPlanations)
- **Web App**: Streamlit
- **Data Handling**: Pandas, NumPy, Scikit-learn
- **Serialization**: Joblib

## 📦 Installation & Setup

1.  **Clone the project** (or navigate to the directory).
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Train the model**:
    ```bash
    python train_model.py
    ```
4.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

## 📊 Dataset
Uses the [UCI Heart Disease Dataset](https://archive.ics.uci.edu/ml/datasets/heart+disease), specifically the Cleveland processed data.

## 🔍 Understanding the SHAP Plot
- **Red bars**: Clinical factors that *increase* the risk score.
- **Blue bars**: Clinical factors that *decrease* the risk score.
- **f(x)**: The model's prediction in log-odds (transformed to % probability in the UI).
