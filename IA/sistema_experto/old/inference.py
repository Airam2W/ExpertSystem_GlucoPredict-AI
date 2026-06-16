from .rules import RULES

def infer_risk(facts):
    risk = 0

    explanations_general = []
    explanations_medical = []
    recommendations = []
    metrics = []
    recomendaciones_con_impacto = []

    diagnostico = "Sin clasificar"
    nivel_riesgo = "Bajo"

    for rule in RULES:
        try:
            if rule["condition"](facts):

                # SUMA DE RIESGO
                risk += rule["impact"]

                # EXPLICACIONES
                explanations_general.append(rule["explication_general"])
                explanations_medical.append(rule["explication_medica"])

                # RECOMENDACIONES
                recommendations.append(rule["recommendation"])

                recomendaciones_con_impacto.append({
                    "recommendation": rule["recommendation"],
                    "impact": rule["impact"]
                })

                # MÉTRICAS
                metric = rule["metric"].copy()
                if callable(metric["value"]):
                    metric["value"] = metric["value"](facts)
                metrics.append(metric)

                # CLASIFICACIÓN (ESCALABLE)
                if rule["type"] == "diagnostico":
                    diagnostico = "Probable Diabetes"
                    nivel_riesgo = "Muy Alto"

                elif rule["type"] == "prediabetes" and diagnostico != "Probable Diabetes":
                    diagnostico = "Prediabetes"
                    nivel_riesgo = "Alto"

        except Exception:
            continue

    # NORMALIZAR RIESGO
    risk = max(0, min(risk, 100))

    # AJUSTE FINAL DE NIVEL
    if risk >= 70:
        nivel_riesgo = "Muy Alto"
    elif risk >= 50:
        nivel_riesgo = "Alto"
    elif risk >= 30:
        nivel_riesgo = "Medio"
    else:
        nivel_riesgo = "Bajo"

    return {
        "porcentajeRiesgo": risk,
        "nivel_riesgo": nivel_riesgo,
        "diagnostico": diagnostico,

        "explicacion_general": explanations_general,
        "explicacion_medica": explanations_medical,

        "recomendaciones": list(set(recommendations)),
        "recomendaciones_con_impacto": recomendaciones_con_impacto,

        "metricas": metrics
    }