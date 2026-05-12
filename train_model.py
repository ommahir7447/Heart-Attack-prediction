"""
HeartGuard AI — Advanced Model Training Pipeline
═══════════════════════════════════════════════════
• Multi-source UCI Heart Disease data (Cleveland + Hungary + Switzerland + VA Long Beach)
• Robust preprocessing with outlier clipping & feature engineering
• Hyperparameter tuning via RandomizedSearchCV
• Stratified K-Fold cross-validation
• XGBoost with optimised parameters
• Comprehensive evaluation (Accuracy, AUC-ROC, Precision, Recall, F1)
"""

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import (
    train_test_split, StratifiedKFold, RandomizedSearchCV, cross_val_score
)
from sklearn.metrics import (
    accuracy_score, classification_report, roc_auc_score,
    confusion_matrix, f1_score, precision_score, recall_score
)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from scipy.stats import uniform, randint
import joblib
import os
import warnings

warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════
# 1. DATA LOADING — Multi-source UCI Heart Disease
# ═══════════════════════════════════════════════════

def load_multi_source_data():
    """Load and combine heart disease datasets from multiple UCI sources."""
    columns = [
        "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
        "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"
    ]

    sources = {
        "Cleveland": "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data",
        "Hungary": "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.hungarian.data",
        "Switzerland": "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.switzerland.data",
        "VA Long Beach": "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.va.data",
    }

    frames = []
    for name, url in sources.items():
        try:
            df = pd.read_csv(url, names=columns, na_values="?")
            df["source"] = name
            frames.append(df)
            print(f"  ✓ {name}: {len(df)} records loaded")
        except Exception as e:
            print(f"  ✗ {name}: failed to load ({e})")

    if not frames:
        raise RuntimeError("Could not load any dataset.")

    combined = pd.concat(frames, ignore_index=True)
    print(f"\n  Total combined records: {len(combined)}")
    return combined


# ═══════════════════════════════════════════════════
# 2. PREPROCESSING & FEATURE ENGINEERING
# ═══════════════════════════════════════════════════

def preprocess(df):
    """Clean data, engineer features, and prepare for training."""

    # Drop source column (not a feature)
    df = df.drop("source", axis=1, errors="ignore")

    # Binary target: 0 = no heart disease, >0 = heart disease
    df["target"] = (df["target"] > 0).astype(int)

    # ── Handle missing values ──
    # Numeric columns: fill with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)

    # Drop rows where too many features are missing (>50%)
    feature_cols = [c for c in df.columns if c != "target"]
    threshold = len(feature_cols) * 0.5
    df = df.dropna(thresh=int(threshold), subset=feature_cols)

    # ── Outlier clipping (IQR method on continuous features) ──
    continuous = ["age", "trestbps", "chol", "thalach", "oldpeak"]
    for col in continuous:
        if col in df.columns:
            q1 = df[col].quantile(0.01)
            q99 = df[col].quantile(0.99)
            df[col] = df[col].clip(lower=q1, upper=q99)

    # ── Feature engineering ──
    # Age risk groups
    df["age_risk"] = pd.cut(df["age"], bins=[0, 40, 55, 70, 120], labels=[0, 1, 2, 3]).astype(float)

    # BP × Cholesterol interaction (both are continuous cardiac risk factors)
    df["bp_chol_interaction"] = df["trestbps"] * df["chol"] / 10000.0

    # Heart rate reserve proxy (higher thalach is protective)
    df["hr_reserve"] = df["thalach"] / (220 - df["age"])

    # ST depression severity flag
    df["st_severe"] = (df["oldpeak"] >= 2.0).astype(int)

    # Age × sex interaction
    df["age_sex"] = df["age"] * df["sex"]

    # Exercise risk composite (exang + oldpeak + slope combined)
    df["exercise_risk"] = df["exang"] + (df["oldpeak"] / 4.0) + (df["slope"] / 2.0)

    # Fill any remaining NaN from feature engineering
    df = df.fillna(0)

    print(f"  Features after engineering: {len(df.columns) - 1}")
    print(f"  Final dataset size: {len(df)} records")
    print(f"  Class distribution: {dict(df['target'].value_counts())}")

    return df


# ═══════════════════════════════════════════════════
# 3. MODEL TRAINING WITH HYPERPARAMETER TUNING
# ═══════════════════════════════════════════════════

def train_optimised_model(X_train, y_train):
    """Train XGBoost with RandomizedSearchCV for hyperparameter optimisation."""

    print("\n  Running hyperparameter search (this may take a minute)...")

    # Parameter distributions for RandomizedSearchCV
    param_distributions = {
        "xgb__n_estimators": randint(100, 500),
        "xgb__max_depth": randint(3, 8),
        "xgb__learning_rate": uniform(0.01, 0.2),
        "xgb__subsample": uniform(0.6, 0.4),
        "xgb__colsample_bytree": uniform(0.6, 0.4),
        "xgb__min_child_weight": randint(1, 7),
        "xgb__gamma": uniform(0, 0.5),
        "xgb__reg_alpha": uniform(0, 1.0),
        "xgb__reg_lambda": uniform(0.5, 2.0),
        "xgb__scale_pos_weight": uniform(0.8, 0.8),
    }

    # Pipeline: scale features → XGBoost
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("xgb", xgb.XGBClassifier(
            eval_metric="logloss",
            random_state=42,
            tree_method="hist",
        ))
    ])

    # Stratified K-Fold for robust evaluation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    search = RandomizedSearchCV(
        pipeline,
        param_distributions=param_distributions,
        n_iter=80,
        scoring="roc_auc",
        cv=cv,
        random_state=42,
        n_jobs=-1,
        verbose=0,
    )

    search.fit(X_train, y_train)

    print(f"\n  Best CV AUC-ROC: {search.best_score_:.4f}")
    print(f"  Best parameters:")
    for k, v in search.best_params_.items():
        name = k.replace("xgb__", "")
        print(f"    {name}: {v:.4f}" if isinstance(v, float) else f"    {name}: {v}")

    return search.best_estimator_


# ═══════════════════════════════════════════════════
# 4. EVALUATION
# ═══════════════════════════════════════════════════

def evaluate_model(model, X_test, y_test, X_train, y_train):
    """Comprehensive model evaluation."""

    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    # Cross-validation on full training set
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="roc_auc")

    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred_proba)
    f1 = f1_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print("\n" + "═" * 50)
    print("  MODEL EVALUATION RESULTS")
    print("═" * 50)
    print(f"\n  Accuracy:    {acc:.4f}  ({acc*100:.1f}%)")
    print(f"  AUC-ROC:     {auc:.4f}")
    print(f"  F1 Score:    {f1:.4f}")
    print(f"  Precision:   {precision:.4f}")
    print(f"  Recall:      {recall:.4f}")
    print(f"\n  5-Fold CV AUC-ROC: {cv_scores.mean():.4f} (± {cv_scores.std():.4f})")
    print(f"  CV Scores: {[f'{s:.4f}' for s in cv_scores]}")
    print(f"\n  Confusion Matrix:")
    print(f"    TN={cm[0][0]}  FP={cm[0][1]}")
    print(f"    FN={cm[1][0]}  TP={cm[1][1]}")
    print(f"\n{classification_report(y_test, y_pred, target_names=['No Disease', 'Heart Disease'])}")

    return {
        "accuracy": acc, "auc_roc": auc, "f1": f1,
        "precision": precision, "recall": recall,
        "cv_auc_mean": cv_scores.mean(), "cv_auc_std": cv_scores.std(),
    }


# ═══════════════════════════════════════════════════
# 5. MAIN
# ═══════════════════════════════════════════════════

def load_and_train():
    print("═" * 50)
    print("  HeartGuard AI — Advanced Model Training")
    print("═" * 50)

    # Step 1: Load data
    print("\n▶ Step 1: Loading multi-source UCI data...")
    df = load_multi_source_data()

    # Step 2: Preprocess & feature engineering
    print("\n▶ Step 2: Preprocessing & feature engineering...")
    df = preprocess(df)

    X = df.drop("target", axis=1)
    y = df["target"]
    feature_names = X.columns.tolist()

    # Step 3: Split (stratified)
    print("\n▶ Step 3: Stratified train/test split (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"  Train: {len(X_train)} | Test: {len(X_test)}")

    # Step 4: Train with hyperparameter tuning
    print("\n▶ Step 4: Training XGBoost with hyperparameter tuning...")
    model = train_optimised_model(X_train, y_train)

    # Step 5: Evaluate
    print("\n▶ Step 5: Evaluating model...")
    metrics = evaluate_model(model, X_test, y_test, X_train, y_train)

    # Step 6: Save
    print("▶ Step 6: Saving model artifacts...")
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)

    joblib.dump(model, os.path.join(model_dir, "heart_attack_model.joblib"))
    joblib.dump(feature_names, os.path.join(model_dir, "feature_names.joblib"))
    joblib.dump(metrics, os.path.join(model_dir, "model_metrics.joblib"))

    print(f"\n  ✓ Model saved to {model_dir}/heart_attack_model.joblib")
    print(f"  ✓ Feature names saved ({len(feature_names)} features)")
    print(f"  ✓ Metrics saved to {model_dir}/model_metrics.joblib")
    print("\n" + "═" * 50)
    print("  Training complete!")
    print("═" * 50)


if __name__ == "__main__":
    load_and_train()
