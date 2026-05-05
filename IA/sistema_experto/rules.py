# rules.py

RULES = [

    {
        "condition": lambda f: f.get("hba1c", 0) >= 6.5,
        "impact": 40,
        "type": "diagnostico",
        "level": "alto",
        "explication_general": "Tu nivel de azúcar promedio en sangre es alto.",
        "explication_medica": "HbA1c ≥ 6.5% cumple criterio ADA de diabetes.",
        "recommendation": "Acudir a consulta médica para confirmación y tratamiento.",
        "metric": {
            "factor": "hba1c",
            "value": lambda f: f.get("hba1c"),
            "threshold": 6.5
        }
    },

    {
        "condition": lambda f: f.get("glucosa", 0) >= 126,
        "impact": 35,
        "type": "diagnostico",
        "level": "alto",
        "explication_general": "Tus niveles de glucosa están elevados.",
        "explication_medica": "Glucosa en ayunas ≥ 126 mg/dL sugiere diabetes.",
        "recommendation": "Realizar estudios confirmatorios (HbA1c u OGTT).",
        "metric": {
            "factor": "glucosa",
            "value": lambda f: f.get("glucosa"),
            "threshold": 126
        }
    },

    {
        "condition": lambda f: 5.7 <= f.get("hba1c", 0) < 6.5,
        "impact": 25,
        "type": "prediabetes",
        "level": "medio",
        "explication_general": "Tus niveles indican riesgo de desarrollar diabetes.",
        "explication_medica": "HbA1c entre 5.7–6.4% = prediabetes.",
        "recommendation": "Mejorar alimentación y aumentar actividad física.",
        "metric": {
            "factor": "hba1c",
            "value": lambda f: f.get("hba1c"),
            "threshold": 5.7
        }
    },

    {
        "condition": lambda f: 100 <= f.get("glucosa", 0) < 126,
        "impact": 20,
        "type": "prediabetes",
        "level": "medio",
        "explication_general": "Tu glucosa está ligeramente elevada.",
        "explication_medica": "Glucosa 100–125 mg/dL = prediabetes.",
        "recommendation": "Monitorear glucosa y mejorar hábitos.",
        "metric": {
            "factor": "glucosa",
            "value": lambda f: f.get("glucosa"),
            "threshold": 100
        }
    },

    {
        "condition": lambda f: f.get("imc", 0) >= 30,
        "impact": 20,
        "type": "riesgo",
        "level": "medio",
        "explication_general": "El sobrepeso aumenta el riesgo.",
        "explication_medica": "IMC ≥ 30 asociado a resistencia a la insulina.",
        "recommendation": "Reducir peso (meta ≥5–7%).",
        "metric": {
            "factor": "imc",
            "value": lambda f: f.get("imc"),
            "threshold": 30
        }
    },

    {
        "condition": lambda f: 25 <= f.get("imc", 0) < 30,
        "impact": 10,
        "type": "riesgo",
        "level": "bajo",
        "explication_general": "Tienes sobrepeso.",
        "explication_medica": "IMC 25–29.9 = sobrepeso.",
        "recommendation": "Aumentar actividad física.",
        "metric": {
            "factor": "imc",
            "value": lambda f: f.get("imc"),
            "threshold": 25
        }
    },

    {
        "condition": lambda f: f.get("presion_sistolica", 0) >= 140,
        "impact": 15,
        "type": "riesgo",
        "level": "medio",
        "explication_general": "La presión alta afecta tu salud.",
        "explication_medica": "HTA ≥140 mmHg aumenta riesgo metabólico.",
        "recommendation": "Controlar presión arterial.",
        "metric": {
            "factor": "presion_sistolica",
            "value": lambda f: f.get("presion_sistolica"),
            "threshold": 140
        }
    },

    {
        "condition": lambda f: f.get("antecedentes_familiares_diabetes") == True,
        "impact": 20,
        "type": "riesgo",
        "level": "medio",
        "explication_general": "Tienes antecedentes familiares.",
        "explication_medica": "Historia familiar incrementa riesgo de DM2.",
        "recommendation": "Realizar chequeos periódicos.",
        "metric": {
            "factor": "antecedentes",
            "value": 1,
            "threshold": 1
        }
    },

    {
        "condition": lambda f: f.get("actividad_fisica") == "sedentario",
        "impact": 15,
        "type": "riesgo",
        "level": "medio",
        "explication_general": "La falta de ejercicio afecta tu salud.",
        "explication_medica": "Sedentarismo aumenta resistencia a insulina.",
        "recommendation": "Realizar ≥150 min de ejercicio por semana.",
        "metric": {
            "factor": "actividad_fisica",
            "value": "sedentario",
            "threshold": "activo"
        }
    },

    {
        "condition": lambda f: f.get("imc", 0) >= 30 and f.get("actividad_fisica") == "sedentario",
        "impact": 15,
        "type": "compuesta",
        "level": "alto",
        "explication_general": "Tu estilo de vida aumenta mucho el riesgo.",
        "explication_medica": "Obesidad + sedentarismo = alto riesgo metabólico.",
        "recommendation": "Cambiar hábitos urgentemente.",
        "metric": {
            "factor": "estilo_vida",
            "value": "alto_riesgo",
            "threshold": "medio"
        }
    },

    {
        "condition": lambda f: f.get("glucosa", 0) < 100 and f.get("hba1c", 0) >= 6.5,
        "impact": 20,
        "type": "compuesta",
        "level": "alto",
        "explication_general": "Hay inconsistencia en tus resultados.",
        "explication_medica": "Glucosa normal pero HbA1c elevada → posible diabetes oculta.",
        "recommendation": "Repetir pruebas y evaluar clínicamente.",
        "metric": {
            "factor": "discordancia",
            "value": 1,
            "threshold": 1
        }
    },

    {
        "condition": lambda f: f.get("hdl", 100) < 40,
        "impact": 10,
        "type": "riesgo",
        "level": "medio",
        "explication_general": "Tu colesterol bueno es bajo.",
        "explication_medica": "HDL bajo aumenta riesgo metabólico.",
        "recommendation": "Mejorar dieta y actividad física.",
        "metric": {
            "factor": "hdl",
            "value": lambda f: f.get("hdl"),
            "threshold": 40
        }
    },

    {
        "condition": lambda f: f.get("trigliceridos", 0) >= 150,
        "impact": 10,
        "type": "riesgo",
        "level": "medio",
        "explication_general": "Tus triglicéridos están elevados.",
        "explication_medica": "Triglicéridos altos asociados a resistencia a la insulina.",
        "recommendation": "Reducir azúcares y grasas.",
        "metric": {
            "factor": "trigliceridos",
            "value": lambda f: f.get("trigliceridos"),
            "threshold": 150
        }
    },

    {
        "condition": lambda f: f.get("imc", 0) >= 30 and f.get("trigliceridos", 0) >= 150,
        "impact": 20,
        "type": "compuesta",
        "level": "alto",
        "explication_general": "Tu cuerpo podría tener dificultad para usar la insulina.",
        "explication_medica": "Obesidad + hipertrigliceridemia → resistencia a la insulina.",
        "recommendation": "Intervención intensiva en estilo de vida.",
        "metric": {
            "factor": "resistencia_insulina",
            "value": 1,
            "threshold": 1
        }
    },

    {
        "condition": lambda f: f.get("glucosa", 0) < 100 and 5.7 <= f.get("hba1c", 0) < 6.5,
        "impact": 20,
        "type": "compuesta",
        "level": "alto",
        "explication_general": "Podrías tener riesgo aunque tu glucosa parezca normal.",
        "explication_medica": "Discordancia glucosa normal + HbA1c elevada.",
        "recommendation": "Realizar OGTT.",
        "metric": {
            "factor": "prediabetes_oculta",
            "value": 1,
            "threshold": 1
        }
    },

    {
        "condition": lambda f: f.get("edad", 0) > 45 and f.get("imc", 0) >= 30 and f.get("actividad_fisica") == "sedentario",
        "impact": 25,
        "type": "compuesta",
        "level": "alto",
        "explication_general": "Tu perfil indica alto riesgo de desarrollar diabetes.",
        "explication_medica": "Patrón tipo FINDRISC (edad + obesidad + sedentarismo).",
        "recommendation": "Evaluación médica completa.",
        "metric": {
            "factor": "findrisc_pattern",
            "value": 1,
            "threshold": 1
        }
    },

    {
        "condition": lambda f: (
            f.get("presion_sistolica", 0) >= 140 and
            f.get("imc", 0) >= 30 and
            f.get("trigliceridos", 0) >= 150
        ),
        "impact": 25,
        "type": "compuesta",
        "level": "alto",
        "explication_general": "Tienes varios factores que afectan tu corazón y metabolismo.",
        "explication_medica": "Síndrome metabólico probable.",
        "recommendation": "Intervención médica integral.",
        "metric": {
            "factor": "riesgo_cardiometabolico",
            "value": 1,
            "threshold": 1
        }
    },

    {
        "condition": lambda f: (
            f.get("antecedentes_familiares_diabetes") and
            (100 <= f.get("glucosa", 0) < 126 or 5.7 <= f.get("hba1c", 0) < 6.5)
        ),
        "impact": 20,
        "type": "compuesta",
        "level": "alto",
        "explication_general": "Tu historial familiar aumenta el riesgo actual.",
        "explication_medica": "Predisposición genética + alteración glucémica.",
        "recommendation": "Seguimiento continuo.",
        "metric": {
            "factor": "genetico_prediabetes",
            "value": 1,
            "threshold": 1
        }
    },


    {
        "condition": lambda f: f.get("actividad_fisica") == "activo",
        "impact": -10,
        "type": "protector",
        "level": "bajo",
        "explication_general": "Tu actividad física reduce el riesgo.",
        "explication_medica": "Ejercicio mejora sensibilidad a la insulina.",
        "recommendation": "Mantener actividad física.",
        "metric": {
            "factor": "proteccion_ejercicio",
            "value": 1,
            "threshold": 1
        }
    },

    {
        "condition": lambda f: f.get("imc", 0) < 25,
        "impact": -10,
        "type": "protector",
        "level": "bajo",
        "explication_general": "Tu peso es adecuado.",
        "explication_medica": "IMC normal reduce riesgo metabólico.",
        "recommendation": "Mantener hábitos saludables.",
        "metric": {
            "factor": "peso_normal",
            "value": 1,
            "threshold": 1
        }
    },

]