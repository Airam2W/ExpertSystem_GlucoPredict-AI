# Clinic Model for SWIRA

import pandas as pd
import numpy as np

from catboost import CatBoostClassifier

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score
)


# ============================================================
# LOAD DATA ENSANUT
# ============================================================

df_MX = pd.read_csv("proccessedDataset/Mexico_procesado.csv")

FEATURES = [
    "edad",
    "Peso",
    "Estatura",
    "imc",
    "glu_suero",
    "hb1ac",
    "insulina",
    "trig",
    "col_hdl",
    "col_ldl",
    "ac_urico",
    "sexo_Hombre",
    "sexo_Mujer"
]

TARGET = "riesgo_diabetes_cat"

X_MX = df_MX[FEATURES]
y_MX = df_MX[TARGET]

# ============================================================
# TRAIN TEST SPLIT ENSANUT
# ============================================================

X_train, X_val, y_train, y_val = train_test_split(
    X_MX, y_MX,
    test_size=0.20,
    random_state=42,
    stratify=y_MX
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
    random_seed=42,
    verbose=False
)

# ============================================================
# TRAIN ON ENSANUT
# ============================================================

cb_model.fit(X_train, y_train)

# ============================================================
# SAVE MODEL
# ============================================================

cb_model.save_model("clinicModel.cbm")

# ============================================================
# PREDICTION
# ============================================================

def clinicPrediction(input_data):
    input_df = pd.DataFrame([input_data])
    y_pred_proba = cb_model.predict_proba(input_df)[:, 1]
    results = y_pred_proba[0].round(4)
    return results
"""
EXAMPLE = {
    "edad": 22,
    "Peso": 80,
    "Estatura": 1.85,
    "imc": 23.37,
    "glu_suero": np.nan,
    "hb1ac": np.nan,
    "insulina": np.nan,
    "trig": np.nan,
    "col_hdl": np.nan,
    "col_ldl": np.nan,
    "ac_urico": np.nan,
    "sexo_Hombre": 1,
    "sexo_Mujer": 0
}"""