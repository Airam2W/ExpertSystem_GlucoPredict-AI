import pandas as pd
import numpy as np

# Diccionario global de traducción para lenguaje amigable
TRADUCCION_VARIABLES = {
    "Age": "Edad", "BMI": "Índice de Masa Corporal (IMC)", "glu_suero": "Glucosa en ayunas",
    "hb1ac": "Hemoglobina Glucosilada (HbA1c)", "insulina": "Insulina", "trig": "Triglicéridos",
    "col_hdl": "Colesterol bueno (HDL)", "col_ldl": "Colesterol malo (LDL)", "ac_urico": "Ácido úrico",
    "HighBP": "Presión arterial alta", "Sex": "Género", "PhysActivity": "Falta de actividad física",
    "Smoker": "Tabaquismo", "Fruits": "Bajo consumo de frutas", "Veggies": "Bajo consumo de verduras",
    "HvyAlcoholConsump": "Consumo alto de alcohol", "DiffWalk": "Dificultad para caminar",
    "MentHlth": "Salud mental / Estrés", "AnyHealthcare": "Acceso a servicios de salud",
    "NoDocbcCost": "Limitación por costos médicos", "Education": "Nivel educativo", "Income": "Nivel de ingresos"
}

def getEYRAnalysis(data, prob_clinica, prob_conductual, model_clinico, model_conductual):
    """
    Método maestro unificado para GlucoPredict-AI (Optimizado para Render sin SHAP).
    Combina CatBoost Feature Importance con el Sistema Experto de las NOM.
    """
    cols_clinicas = ["Age", "BMI", "glu_suero", "hb1ac", "insulina", "trig",
                     "col_hdl", "col_ldl", "ac_urico", "HighBP", "Sex"]
    cols_conductuales = ["PhysActivity", "Smoker", "Fruits", "Veggies",
                         "HvyAlcoholConsump", "DiffWalk", "MentHlth",
                         "AnyHealthcare", "NoDocbcCost", "Education", "Income"]

    # 1. Feature Importances con fallback
    try:
        importances_clinicas = dict(zip(cols_clinicas, model_clinico.get_feature_importance()))
    except Exception as e:
        print(f"[ERROR LOG] Fallo al obtener importancias clínicas: {e}")
        importances_clinicas = dict(zip(cols_clinicas, [0]*len(cols_clinicas)))

    try:
        importances_conductuales = dict(zip(cols_conductuales, model_conductual.get_feature_importance()))
    except Exception as e:
        print(f"[ERROR LOG] Fallo al obtener importancias conductuales: {e}")
        importances_conductuales = dict(zip(cols_conductuales, [0]*len(cols_conductuales)))

    # 2. Submódulos con protección individual try/except
    try:
        analisis = getAnalisis(data, prob_clinica, prob_conductual,
                               importances_clinicas, importances_conductuales)
    except Exception as e:
        print(f"[ERROR LOG] Fallo en getAnalisis con data={data}: {e}")
        analisis = "No se pudo generar el análisis por un error interno."

    try:
        listaExplicaciones = getExplicaciones(data,
                                              importances_clinicas,
                                              importances_conductuales)
    except Exception as e:
        print(f"[ERROR LOG] Fallo en getExplicaciones con data={data}: {e}")
        listaExplicaciones = ["No se pudieron generar las explicaciones por un error interno."]

    try:
        listaRecomendaciones = getRecomendaciones(data,
                                                  importances_clinicas,
                                                  importances_conductuales)
    except Exception as e:
        print(f"[ERROR LOG] Fallo en getRecomendaciones con data={data}: {e}")
        listaRecomendaciones = ["No se pudieron generar las recomendaciones por un error interno."]

    return {
        "analisis": analisis,
        "explicaciones": listaExplicaciones,
        "recomendaciones": listaRecomendaciones
    }


def getAnalisis(data, prob_clinica, prob_conductual, imp_clinicas, imp_conductuales):
    """Genera el bloque informativo 'Lo que encontramos' basándose en factores de riesgo activos."""
    factores_riesgo_tuplas = []
    
    try:
        if data.get("glu_suero") is not None and data["glu_suero"] >= 100: 
            factores_riesgo_tuplas.append((TRADUCCION_VARIABLES["glu_suero"], imp_clinicas.get("glu_suero", 0)))
        if data.get("hb1ac") is not None and data["hb1ac"] >= 5.7: 
            factores_riesgo_tuplas.append((TRADUCCION_VARIABLES["hb1ac"], imp_clinicas.get("hb1ac", 0)))
        if data.get("BMI") is not None and data["BMI"] >= 25.0: 
            factores_riesgo_tuplas.append((TRADUCCION_VARIABLES["BMI"], imp_clinicas.get("BMI", 0)))
        if data.get("HighBP") is not None and data["HighBP"] == 1: 
            factores_riesgo_tuplas.append((TRADUCCION_VARIABLES["HighBP"], imp_clinicas.get("HighBP", 0)))
        if data.get("Age") is not None and data["Age"] >= 45: 
            factores_riesgo_tuplas.append((TRADUCCION_VARIABLES["Age"], imp_clinicas.get("Age", 0)))
        if data.get("PhysActivity") is not None and data["PhysActivity"] == 0: 
            factores_riesgo_tuplas.append((TRADUCCION_VARIABLES["PhysActivity"], imp_conductuales.get("PhysActivity", 0)))
        if data.get("Smoker") is not None and data["Smoker"] == 1: 
            factores_riesgo_tuplas.append((TRADUCCION_VARIABLES["Smoker"], imp_conductuales.get("Smoker", 0)))
        if data.get("trig") is not None and data["trig"] >= 150: 
            factores_riesgo_tuplas.append((TRADUCCION_VARIABLES["trig"], imp_clinicas.get("trig", 0)))
        if data.get("col_hdl") is not None and data["col_hdl"] < 40:
            factores_riesgo_tuplas.append((TRADUCCION_VARIABLES["col_hdl"], imp_clinicas.get("col_hdl", 0)))
        if data.get("HvyAlcoholConsump") is not None and data["HvyAlcoholConsump"] == 1:
            factores_riesgo_tuplas.append((TRADUCCION_VARIABLES["HvyAlcoholConsump"], imp_conductuales.get("HvyAlcoholConsump", 0)))
    except Exception as e:
        print(f"[ERROR LOG] Error procesando umbrales en getAnalisis: {e}")

    factores_riesgo_tuplas.sort(key=lambda x: x[1], reverse=True)
    factores_riesgo = [f[0] for f in factores_riesgo_tuplas]

    if factores_riesgo:
        if len(factores_riesgo) > 1:
            lista_texto = ", ".join(factores_riesgo[:-1]) + " y " + factores_riesgo[-1] + " fueron los factores que causan que se tenga"
        else:
            lista_texto = factores_riesgo[0] + " fue el factor que causa que se tenga"
    else:
        lista_texto = "ningún factor de riesgo evidente evaluado en este momento fue detectado, y eso hace que se tenga"

    p_clinica_str = f"{round(prob_clinica, 1)}%"
    p_conductual_str = f"{round(prob_conductual, 1)}%"

    return (
        f"Al realizar el análisis de la predicción Clínica y Conductual nos dimos cuenta que \n"
        f"{lista_texto} {p_clinica_str} en su riesgo Clínico "
        f"y {p_conductual_str} en su riesgo Conductual."
    )


def getExplicaciones(data, imp_clinicas, imp_conductuales):
    """Sistema Experto: 'Por qué salió así'. Prioriza y ordena explicaciones con lenguaje claro."""
    listaExplicaciones = []
    
    age = data.get("Age")
    bmi = data.get("BMI")
    glu = data.get("glu_suero")
    hb1ac = data.get("hb1ac")
    high_bp = data.get("HighBP")
    phys_act = data.get("PhysActivity")
    smoker = data.get("Smoker")
    trig = data.get("trig")
    col_hdl = data.get("col_hdl")
    alcohol = data.get("HvyAlcoholConsump")
    
    altas, medias, bajas = [], [], []
    
    # --- Evaluación Glucosa y HbA1c ---
    try:
        w_glu = round(imp_clinicas.get("glu_suero", 0.0), 1)
        w_hb = round(imp_clinicas.get("hb1ac", 0.0), 1)
        w_max_met = max(w_glu, w_hb)
        
        if glu is not None or hb1ac is not None:
            if (glu is not None and glu >= 126) or (hb1ac is not None and hb1ac >= 6.5):
                txt = f"Tu nivel de azúcar ({glu if glu is not None else 'N/A'} mg/dL) o tu promedio de los últimos meses ({hb1ac if hb1ac is not None else 'N/A'}%) están muy altos según los rangos médicos del país. Este factor influye en un {w_glu}% en tu resultado clínico."
                altas.append((txt, w_max_met))
            elif (glu is not None and 100 <= glu < 126) or (hb1ac is not None and 5.7 <= hb1ac < 6.49):
                txt = f"Tu azúcar en ayunas ({glu if glu is not None else 'N/A'} mg/dL) o tu promedio de glucosa ({hb1ac if hb1ac is not None else 'N/A'}%) salieron un poco elevados. Esto indica prediabetes, pero estás muy a tiempo de corregirlo (Este factor influye: {w_max_met}%)."
                medias.append((txt, w_max_met))
    except Exception as e:
        print(f"[ERROR LOG] Fallo en evaluación de Metabolismo: {e}")
        
    # --- Evaluación IMC ---
    try:
        w_bmi = round(imp_clinicas.get("BMI", 0.0), 1)
        if bmi is not None:
            if bmi >= 30.0:
                txt = f"Tu peso está en rango de obesidad para tu estatura (IMC: {bmi}). El exceso de grasa hace que a tu cuerpo le cueste más trabajo aprovechar el azúcar, aportando un {w_bmi}% de peso a tu riesgo."
                altas.append((txt, w_bmi))
            elif 25.0 <= bmi < 30.0:
                txt = f"Tienes un poco de sobrepeso (IMC: {bmi}). Esto le exige un esfuerzo extra a tu cuerpo para procesar la glucosa, con una relevancia del {w_bmi}%."
                medias.append((txt, w_bmi))
    except Exception as e:
        print(f"[ERROR LOG] Fallo en evaluación de IMC: {e}")
        
    # --- Evaluación Lípidos (Triglicéridos y Colesterol) ---
    try:
        w_trig = round(imp_clinicas.get("trig", 0.0), 1)
        w_hdl = round(imp_clinicas.get("col_hdl", 0.0), 1)
        if trig is not None and trig >= 150:
            txt = f"Tus triglicéridos ({trig} mg/dL) están por encima del límite recomendado. El exceso de grasas en la sangre se asocia con mayor dificultad para controlar el azúcar (Este factor influye: {w_trig}%)."
            medias.append((txt, w_trig))
        if col_hdl is not None and col_hdl < 40:
            txt = f"Tu colesterol bueno o protector ({col_hdl} mg/dL) está bajo. Al tener menos 'escudos' de colesterol bueno, aumenta la probabilidad de problemas metabólicos (Este factor influye: {w_hdl}%)."
            medias.append((txt, w_hdl))
    except Exception as e:
        print(f"[ERROR LOG] Fallo en evaluación de Lípidos: {e}")

    # --- Regla Compleja (Edad + Hipertensión + Peso) ---
    try:
        w_age = round(imp_clinicas.get("Age", 0.0), 1)
        w_bp = round(imp_clinicas.get("HighBP", 0.0), 1)
        
        if age is not None and high_bp is not None and bmi is not None:
            if age >= 45 and high_bp == 1 and bmi >= 25.0:
                txt = f"Tu edad ({age} años), junto con la presión alta y el exceso de peso, se juntan para formar una combinación delicada que eleva bastante tu puntaje general de riesgo (Peso sumado del {round(w_age + w_bp + w_bmi, 1)}%)."
                altas.append((txt, max(w_age, w_bp, w_bmi)))
            else:
                if high_bp == 1:
                    txt = f"Tienes la presión arterial alta. Las guías de salud señalan que esto cansa más rápido a tu sistema del corazón y la circulación (Este factor influye: {w_bp}%)."
                    medias.append((txt, w_bp))
                if age >= 45:
                    txt = f"Tienes {age} años. Al pasar los 45 años, las células del cuerpo se vuelven un poco menos eficientes para procesar los alimentos de forma natural (Este factor influye: {w_age}%)."
                    bajas.append((txt, w_age))
        else:
            if high_bp == 1:
                txt = f"Tienes la presión arterial alta. Las guías de salud señalan que esto cansa más rápido a tu sistema del corazón y la circulación (Este factor influye: {w_bp}%)."
                medias.append((txt, w_bp))
            if age is not None and age >= 45:
                txt = f"Tienes {age} años. Al pasar los 45 años, las células del cuerpo se vuelven un poco menos eficientes para procesar los alimentos de forma natural (Este factor influye: {w_age}%)."
                bajas.append((txt, w_age))
    except Exception as e:
        print(f"[ERROR LOG] Fallo en evaluación de Regla Compleja/Edad/Presión: {e}")

    # --- Evaluación Conductual ---
    try:
        w_phys = round(imp_conductuales.get("PhysActivity", 0.0), 1)
        if phys_act is not None and phys_act == 0:
            txt = f"Hacer poca actividad física impide que tus músculos quemen el azúcar de la comida como energía, influyendo en tu riesgo diario con un peso del {w_phys}%."
            medias.append((txt, w_phys))
            
        w_smoke = round(imp_conductuales.get("Smoker", 0.0), 1)
        if smoker is not None and smoker == 1:
            txt = f"El consumo de tabaco desgasta y oxigena mal tus células, lo que contribuye a que tu cuerpo batalle más en sus funciones con una relevancia del {w_smoke}%."
            bajas.append((txt, w_smoke))

        w_alc = round(imp_conductuales.get("HvyAlcoholConsump", 0.0), 1)
        if alcohol is not None and alcohol == 1:
            txt = f"El consumo frecuente de alcohol interrumpe las tareas de tu hígado y causa picos drásticos de azúcar que no le hacen bien a tu organismo (Este factor influye: {w_alc}%)."
            medias.append((txt, w_alc))
    except Exception as e:
        print(f"[ERROR LOG] Fallo en evaluación Conductual: {e}")

    # Ordenar por importancia real antes del render
    altas.sort(key=lambda x: x[1], reverse=True)
    medias.sort(key=lambda x: x[1], reverse=True)
    bajas.sort(key=lambda x: x[1], reverse=True)

    if altas or medias or bajas:
        for txt, w in altas: listaExplicaciones.append(f"🚨 {txt}")
        for txt, w in medias: listaExplicaciones.append(f"⚠️ {txt}")
        for txt, w in bajas: listaExplicaciones.append(f"ℹ️ {txt}")
    else:
        preventivos = []
        if glu is not None:
            preventivos.append((f"🛡️ ¡Excelente! Tu nivel de azúcar en ayunas ({glu} mg/dL) se encuentra en un rango muy saludable (Este factor influye: {round(imp_clinicas.get('glu_suero',0),1)}%).", imp_clinicas.get('glu_suero', 0)))
        if bmi is not None:
            preventivos.append((f"🛡️ Tu peso actual con respecto a tu estatura (IMC: {bmi}) es el ideal, lo que protege tu salud (Este factor influye: {round(imp_clinicas.get('BMI',0),1)}%).", imp_clinicas.get('BMI', 0)))
        if phys_act is not None and phys_act == 1:
            preventivos.append((f"🛡️ Mantenerte activo con ejercicio ayuda muchísimo a que tu cuerpo regule el azúcar de forma completamente natural (Este factor influye: {round(imp_conductuales.get('PhysActivity',0),1)}%).", imp_conductuales.get('PhysActivity', 0)))
        
        preventivos.sort(key=lambda x: x[1], reverse=True)
        listaExplicaciones = [p[0] for p in preventivos]

    return listaExplicaciones


def getRecomendaciones(data, imp_clinicas, imp_conductuales):
    """Sistema Experto: 'Te recomendamos lo siguiente'. Prescribe metas de forma clara y sin alarmar."""
    listaRecomendaciones = []
    
    age = data.get("Age")
    bmi = data.get("BMI")
    glu = data.get("glu_suero")
    hb1ac = data.get("hb1ac")
    high_bp = data.get("HighBP")
    phys_act = data.get("PhysActivity")
    smoker = data.get("Smoker")
    trig = data.get("trig")
    col_hdl = data.get("col_hdl")
    alcohol = data.get("HvyAlcoholConsump")
    fruits = data.get("Fruits")
    veggies = data.get("Veggies")
    
    altas, medias, bajas = [], [], []

    # --- Criterios de activación por riesgo detectado ---
    try:
        if glu is not None or hb1ac is not None:
            w = max(imp_clinicas.get("glu_suero", 0), imp_clinicas.get("hb1ac", 0))
            if (glu is not None and glu >= 126) or (hb1ac is not None and hb1ac >= 6.5):
                altas.append(("Es muy importante agendar una cita médica pronto. Es necesario realizar una nueva prueba de laboratorio para revisar con certeza tus niveles de azúcar.", w))
            elif (glu is not None and 100 <= glu < 126) or (hb1ac is not None and 5.7 <= hb1ac < 6.5):
                medias.append(("Estás en el momento perfecto para actuar (Prediabetes). Con solo bajar el consumo de refrescos, jugos, harinas refinadas y pan dulce, tus niveles pueden volver a la normalidad.", w))
    except Exception as e:
        print(f"[ERROR LOG] Fallo en recomendaciones de Metabolismo: {e}")

    try:
        if bmi is not None:
            w = imp_clinicas.get("BMI", 0)
            if bmi >= 30.0:
                altas.append((f"Con tu IMC actual ({bmi}), la meta recomendada por salud es ir bajando un poco de peso de forma lenta y constante. Esto quitará la resistencia en tus células.", w))
            elif 25.0 <= bmi < 30.0:
                medias.append(("Intenta cuidar el tamaño de tus porciones al comer. Ajustar un poco tu peso actual evitará que sigas subiendo y le dará un gran respiro a tu cuerpo.", w))
    except Exception as e:
        print(f"[ERROR LOG] Fallo en recomendaciones de Peso: {e}")

    try:
        if trig is not None and trig >= 150:
            medias.append(("Bájale un poco a los alimentos empaquetados o fritos. Tu cuerpo convierte el exceso de azúcares y harinas directamente en grasa para la sangre.", imp_clinicas.get("trig", 0)))
        if col_hdl is not None and col_hdl < 40:
            medias.append(("Agrega a tu comida grasas de las buenas, como aguacate, aceite de oliva o un puño de cacahuates/almendras, para subir tu colesterol protector.", imp_clinicas.get("col_hdl", 0)))
    except Exception as e:
        print(f"[ERROR LOG] Fallo en recomendaciones de Dislipidemia: {e}")

    try:
        if age is not None and high_bp is not None and bmi is not None and age >= 45 and high_bp == 1 and bmi >= 25.0:
            altas.append(("Tu perfil necesita atención integral: procura checar tu presión seguido y trata de usar menos sal al cocinar para proteger tu corazón.", max(imp_clinicas.get("Age", 0), imp_clinicas.get("HighBP", 0))))
        else:
            if high_bp is not None and high_bp == 1: 
                medias.append(("Evita los alimentos muy salados o enlatados para ayudar a que tus arterias no se fuercen de más.", imp_clinicas.get("HighBP", 0)))
            if age is not None and age >= 45: 
                bajas.append(("Al cumplir más de 45 años, es un excelente hábito realizarse estudios básicos de sangre por lo menos una vez al año para vigilar que todo vaya bien.", imp_clinicas.get("Age", 0)))
    except Exception as e:
        print(f"[ERROR LOG] Fallo en recomendaciones de Sinergia/Cardio: {e}")

    try:
        if phys_act is not None and phys_act == 0:
            medias.append(("Sigue la meta recomendada: intenta acumular al menos 2 horas y media de ejercicio a la semana (por ejemplo, caminar rápido 30 minutos al día, 5 días a la semana).", imp_conductuales.get("PhysActivity", 0)))
        if smoker is not None and smoker == 1:
            bajas.append(("Considera reducir o dejar el cigarro. Fumar acelera el desgaste en los pequeños vasos sanguíneos, complicando el control del azúcar.", imp_conductuales.get("Smoker", 0)))
        if alcohol is not None and alcohol == 1:
            medias.append(("Modera o disminuye el consumo de alcohol. Esto le ayudará a tu hígado a limpiarse y a que tus células procesen mejor la glucosa.", imp_conductuales.get("HvyAlcoholConsump", 0)))
        if fruits is not None and fruits == 1:
            bajas.append(("Trata de comer un poco más de fruta entera fresca en lugar de tomar jugos; la fruta entera te da fibra que evita picos de azúcar.", imp_conductuales.get("Fruits", 0)))
        if veggies is not None and veggies == 1:
            bajas.append(("Intenta que la mitad de tu plato tenga verduras o ensalada. Te darán defensas naturales y mantendrán tu digestión al cien.", imp_conductuales.get("Veggies", 0)))
    except Exception as e:
        print(f"[ERROR LOG] Fallo en recomendaciones Conductuales: {e}")

    # Ordenar de mayor a menor importancia
    altas.sort(key=lambda x: x[1], reverse=True)
    medias.sort(key=lambda x: x[1], reverse=True)
    bajas.sort(key=lambda x: x[1], reverse=True)

    if altas or medias or bajas:
        for rec, w in altas: listaRecomendaciones.append(f"🔴⏰ {rec}")
        for rec, w in medias: listaRecomendaciones.append(f"🟠📌 {rec}")
        for rec, w in bajas: listaRecomendaciones.append(f"🟢📝 {rec}")
    else:
        preventivas = [
            ("🧩 Vas por excelente camino. Sigue manteniendo una alimentación balanceada, rica en verduras y baja en grasas saturadas.", imp_clinicas.get("BMI", 0)),
            ("🛡️ Sigue revisando tus niveles de azúcar en ayunas una vez al año como una excelente costumbre de prevención.", imp_clinicas.get("glu_suero", 0))
        ]
        if phys_act is not None and phys_act == 1:
            preventivas.append(("🧩 Sigue manteniendo tu rutina de ejercicio semanal; esto mantiene a tus células fuertes y sanas.", imp_conductuales.get("PhysActivity", 0)))
        
        preventivas.sort(key=lambda x: x[1], reverse=True)
        listaRecomendaciones = [p[0] for p in preventivas]

    return listaRecomendaciones

def unificarData(historial):
    data = {}

    # Copiar todo lo clínico
    for k, v in historial.get("clinico", {}).items():
        data[k] = v

    # Copiar todo lo conductual
    for k, v in historial.get("conductual", {}).items():
        data[k] = v

    # Priorizar Age sobre edad
    if "Age" in data:
        data["Age"] = data["Age"]
        data.pop("edad", None)

    # Priorizar BMI sobre imc
    if "BMI" in data:
        data["BMI"] = data["BMI"]
        data.pop("imc", None)

    # Priorizar Sex sobre sexo_Hombre/sexo_Mujer
    if "Sex" in data:
        data["Sex"] = data["Sex"]
        data.pop("sexo_Hombre", None)
        data.pop("sexo_Mujer", None)

    return data