import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def load_and_train():
    # URL for UCI Heart Disease Dataset (Cleveland)
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
    columns = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", 
               "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"]
    
    # Load dataset
    print("Downloading dataset...")
    df = pd.read_csv(url, names=columns, na_values="?")
    
    # Simple data cleaning: UCI Cleveland has '?' for missing values
    df = df.fillna(df.median())
    
    # Binary classification: 0 = No heart disease, >0 = Heart disease
    df['target'] = (df['target'] > 0).astype(int)
    
    X = df.drop("target", axis=1)
    y = df["target"]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train XGBoost model
    print("Training XGBoost model...")
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Model Accuracy: {acc:.2f}")
    print(classification_report(y_test, preds))
    
    # Save model and feature names
    print("Saving model artifacts...")
    model_dir = "models"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    joblib.dump(model, os.path.join(model_dir, "heart_attack_model.joblib"))
    joblib.dump(X.columns.tolist(), os.path.join(model_dir, "feature_names.joblib"))
    
    print("Training complete.")

if __name__ == "__main__":
    load_and_train()
