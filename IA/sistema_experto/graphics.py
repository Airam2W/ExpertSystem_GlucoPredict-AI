def to_number(val):
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        try:
            return float(val.strip())
        except ValueError:
            return None
    return None

def classify_risk(value, thresholds, label=""):
    v = to_number(value)
    print(f"[DEBUG] {label} valor bruto={value} convertido={v}")
    if v is None:
        return ("Sin dato", "bajo")
    if v >= thresholds["alto"]:
        print(f"[DEBUG] {label} → ALTO")
        return (v, "alto")
    elif v >= thresholds["medio"]:
        print(f"[DEBUG] {label} → MEDIO")
        return (v, "medio")
    else:
        print(f"[DEBUG] {label} → BAJO")
        return (v, "bajo")

def getMetrics(clinico, conductual):
    print("[DEBUG] Datos clínicos recibidos:", clinico)
    print("[DEBUG] Datos conductuales recibidos:", conductual)

    radar = {
        "labels": ["Glucosa", "HbA1c", "IMC", "Colesterol LDL", "Colesterol HDL", "Triglicéridos"],
        "values": []
    }

    # Glucosa
    glu, glu_risk = classify_risk(clinico.get("glu_suero"), {"medio": 100, "alto": 126}, "Glucosa")
    radar["values"].append({"label": "Glucosa", "value": glu, "impact": glu_risk, "unit": "mg/dL"})

    # HbA1c
    hb, hb_risk = classify_risk(clinico.get("hb1ac"), {"medio": 5.7, "alto": 6.5}, "HbA1c")
    radar["values"].append({"label": "HbA1c", "value": hb, "impact": hb_risk, "unit": "%"})

    # IMC
    bmi, bmi_risk = classify_risk(clinico.get("imc"), {"medio": 25, "alto": 30}, "IMC")
    radar["values"].append({"label": "IMC", "value": bmi, "impact": bmi_risk, "unit": "kg/m²"})

    # LDL
    ldl, ldl_risk = classify_risk(clinico.get("col_ldl"), {"medio": 100, "alto": 160}, "Colesterol LDL")
    radar["values"].append({"label": "Colesterol LDL", "value": ldl, "impact": ldl_risk, "unit": "mg/dL"})

    # HDL (inverso: bajo es riesgo)
    hdl = to_number(clinico.get("col_hdl"))
    print(f"[DEBUG] HDL valor bruto={clinico.get('col_hdl')} convertido={hdl}")
    if hdl is not None:
        if hdl < 40:
            hdl_risk = "alto"
        elif hdl < 60:
            hdl_risk = "medio"
        else:
            hdl_risk = "bajo"
    else:
        hdl_risk = "bajo"
    radar["values"].append({"label": "Colesterol HDL", "value": hdl, "impact": hdl_risk, "unit": "mg/dL"})

    # Triglicéridos
    trig, trig_risk = classify_risk(clinico.get("trig"), {"medio": 150, "alto": 200}, "Triglicéridos")
    radar["values"].append({"label": "Triglicéridos", "value": trig, "impact": trig_risk, "unit": "mg/dL"})

    # =========================
    # FACTORES CONDUCTUALES
    # =========================
    risk_factors = []

    if conductual.get("Smoker") == 1:
        print("[DEBUG] Conductual: Smoker=1 → Tabaquismo HIGH")
        risk_factors.append({"name": "Tabaquismo", "impact": "alto"})
    if conductual.get("PhysActivity") == 0:
        print("[DEBUG] Conductual: PhysActivity=0 → Sedentarismo MEDIUM")
        risk_factors.append({"name": "Sedentarismo", "impact": "medio"})
    if conductual.get("HvyAlcoholConsump") == 1:
        print("[DEBUG] Conductual: HvyAlcoholConsump=1 → Alcohol MEDIUM")
        risk_factors.append({"name": "Consumo de alcohol", "impact": "medio"})
    if conductual.get("HighBP") == 1:
        print("[DEBUG] Conductual: HighBP=1 → Hipertensión HIGH")
        risk_factors.append({"name": "Hipertensión", "impact": "alto"})

    return {"radar": radar, "risk_factors": risk_factors}