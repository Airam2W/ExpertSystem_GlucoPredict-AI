# Intermediary of Clinic Model & Conductual Model

import pickle

import pandas as pd
from catboost import CatBoostClassifier
import os
from IA.sistema_experto.graphics import getMetrics
from IA.sistema_experto.eyra import getEYRAnalysis, unificarData



def clinicPrediction(input_data):
    model = CatBoostClassifier()
    model_path = os.path.join(os.path.dirname(__file__), "clinicModel.cbm")
    model.load_model(model_path)
    input_df = pd.DataFrame([input_data])
    y_pred_proba = model.predict_proba(input_df)[:, 1]
    results = y_pred_proba[0].round(4)
    results_porcent = round(results * 100, 2)
    return results_porcent

def conductualPrediction(input_data):
    model = CatBoostClassifier()
    model_path = os.path.join(os.path.dirname(__file__), "conductualModel.cbm")
    model.load_model(model_path)
    input_df = pd.DataFrame([input_data])
    y_pred_proba = model.predict_proba(input_df)[:, 1]
    results = y_pred_proba[0].round(4)
    results_porcent = round(results * 100, 2)
    return results_porcent

def getMetricas(historial):
    clinico = historial.get("clinico", {})
    conductual = historial.get("conductual", {})
    return getMetrics(clinico, conductual)
    
def getEYRA(historial):
    dataUnificada = unificarData(historial)
    prob_clinica = clinicPrediction(historial.get("clinico", {}))
    prob_conductual = conductualPrediction(historial.get("conductual", {}))
    model_clinico = CatBoostClassifier()
    model_clinico.load_model(os.path.join(os.path.dirname(__file__), "clinicModel.cbm"))
    model_conductual = CatBoostClassifier()
    model_conductual.load_model(os.path.join(os.path.dirname(__file__), "conductualModel.cbm"))

    eyra = getEYRAnalysis(dataUnificada, prob_clinica, prob_conductual, model_clinico, model_conductual)
    return eyra