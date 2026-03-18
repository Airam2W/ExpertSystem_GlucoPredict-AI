from .rules import RULES

def infer_risk(facts):
    risk = 0
    explanations_general = []
    explanations_medical = []
    recommendations = []
    metrics = []
    recomendaciones_con_impacto = []

    for rule in RULES:
        try:
            if rule["condition"](facts):
                risk += rule["impact"]

                explanations_general.append(rule["explication_general"])
                explanations_medical.append(rule["explication_medica"])
                recommendations.append(rule["recommendation"])

                recomendaciones_con_impacto.append({
                    "recommendation": rule["recommendation"],
                    "impact": rule["impact"]
                })

                metric = rule["metric"].copy()
                if callable(metric["value"]):
                    metric["value"] = metric["value"](facts)
                metrics.append(metric)

        except Exception:
            continue

    return {
        "porcentajeRiesgo": min(risk, 100),
        "explicacion_general": explanations_general,
        "explicacion_medica": explanations_medical,
        "recomendaciones": list(set(recommendations)),
        "recomendaciones_con_impacto": recomendaciones_con_impacto,
        "metricas": metrics
    }