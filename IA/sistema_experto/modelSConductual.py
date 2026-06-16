# Conductual Model for SWIRA

import pandas as pd
import numpy as np

from catboost import CatBoostClassifier

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score
)

# ============================================================
# LOAD DATA
# ============================================================
df = pd.read_csv(
    "proccessedDataset/DHI_procesado.csv"
)

# ============================================================
# FEATURES
# ============================================================

FEATURES = [
    "PhysActivity_1.0",
    "Smoker_1.0",
    "HighBP_1.0",
    "Fruits_1.0",
    "BMI",
    "Sex_1.0", # 0: Female, 1: Male
    "Age",
    "Veggies_1.0",
    "HvyAlcoholConsump_1.0",
    "DiffWalk_1.0",
    "MentHlth",
    "AnyHealthcare_1.0",
    "NoDocbcCost_1.0",
    "Education",
    "Income",
]

FEATURES_CAMBIAR = [
    "PhysActivity",
    "Smoker",
    "HighBP",
    "Fruits",
    "BMI",
    "Sex", # 0: Female, 1: Male
    "Age",
    "Veggies",
    "HvyAlcoholConsump",
    "DiffWalk",
    "MentHlth",
    "AnyHealthcare",
    "NoDocbcCost",
    "Education",
    "Income",
]

TARGET = "Diabetes_012"

X = df[FEATURES]
X.columns = FEATURES_CAMBIAR
y = df[TARGET]

# ============================================================
# TRAIN TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ============================================================
# MODEL
# ============================================================

cb_model = CatBoostClassifier(
    iterations=500,
    depth=6,
    learning_rate=0.05,
    loss_function="Logloss",
    eval_metric="AUC",
    auto_class_weights="Balanced",
    random_seed=42,
    verbose=False
)

cb_model.fit(X_train, y_train)

# ============================================================
# SAVE MODEL
# ============================================================

cb_model.save_model("conductualModel.cbm")

# ============================================================
# PREDICTION
# ============================================================

def conductualPrediction(input_data):
    input_df = pd.DataFrame([input_data])
    y_pred_proba = cb_model.predict_proba(input_df)[:, 1]
    results = y_pred_proba[0].round(4)
    return results

"""EXAMPLE = {
    "PhysActivity": 0,
    "Smoker": 0,
    "HighBP": np.nan,
    "Fruits": 1,
    "BMI": 23.0,
    "Sex": 1,
    "Age": 22,
    "Veggies": 1,
    "HvyAlcoholConsump": 0,
    "DiffWalk": 0,
    "MentHlth": 15,
    "AnyHealthcare": 1,
    "NoDocbcCost": 0,
    "Education": np.nan,
    "Income": np.nan
}"""