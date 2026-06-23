# 🩺 GlucoPredict-AI — Sistema Experto de Predicción de Diabetes

> **Herramienta de apoyo clínico y conductual para la detección temprana del riesgo de diabetes, basada en inteligencia artificial y las normas oficiales de salud de México (NOM).**

---

## 📌 ¿Qué es GlucoPredict-AI — Sistema Experto de Predicción de Diabetes?

**GlucoPredict-AI — Sistema Experto de Predicción de Diabetes** es un sistema experto inteligente que combina modelos de aprendizaje automático con reglas clínicas y conductuales para evaluar el riesgo de diabetes de un paciente. El sistema genera predicciones personalizadas, explicaciones comprensibles y recomendaciones accionables en lenguaje claro y amigable.

El corazón del sistema es **EYRA** (*Explicaciones Y Recomendaciones Analisis*), un módulo que interpreta los resultados de los modelos de IA y los traduce en mensajes útiles para el usuario, priorizando los factores de riesgo más relevantes según su peso estadístico real.

---

## 🏗️ Arquitectura del Sistema

```
GlucoPredict-AI/
│
├── IA/
│   ├── api/
│   │   └── app.py                  # API REST con Flask
│   │
│   └── sistema_experto/
│       ├── eyra.py                 # Motor de análisis experto (EYRA)
│       ├── graphics.py             # Métricas visuales (radar + factores de riesgo)
│       ├── modelSClinic.py         # Entrenamiento del modelo clínico
│       ├── modelSConductual.py     # Entrenamiento del modelo conductual
│       └── modelSUnificate.py      # Orquestador: une ambos modelos
│
├── proccessedDataset/
│   ├── Mexico_procesado.csv        # Dataset ENSANUT (modelo clínico)
│   └── DHI_procesado.csv           # Dataset conductual
│
├── requirements.txt
└── README.md
```

---

## 🤖 Modelos de Inteligencia Artificial

El sistema utiliza **dos modelos CatBoost** independientes que evalúan distintas dimensiones del riesgo:

### 🔬 Modelo Clínico
Entrenado con datos del estudio **ENSANUT (México)**. Evalúa indicadores biométricos y de laboratorio:

| Variable | Descripción |
|---|---|
| `edad` | Edad del paciente |
| `imc` | Índice de Masa Corporal |
| `glu_suero` | Glucosa en ayunas (mg/dL) |
| `hb1ac` | Hemoglobina Glucosilada (%) |
| `insulina` | Nivel de insulina |
| `trig` | Triglicéridos (mg/dL) |
| `col_hdl` | Colesterol bueno HDL (mg/dL) |
| `col_ldl` | Colesterol malo LDL (mg/dL) |
| `ac_urico` | Ácido úrico |
| `HighBP` | Presión arterial alta |
| `Sex` | Género (0: Mujer, 1: Hombre) |

### 🧠 Modelo Conductual
Entrenado con datos del dataset **DHI**. Evalúa hábitos de vida y factores socioeconómicos:

| Variable | Descripción |
|---|---|
| `PhysActivity` | Actividad física (0: sedentario) |
| `Smoker` | Tabaquismo |
| `Fruits` / `Veggies` | Consumo de frutas y verduras |
| `HvyAlcoholConsump` | Consumo elevado de alcohol |
| `DiffWalk` | Dificultad para caminar |
| `MentHlth` | Salud mental / estrés |
| `AnyHealthcare` | Acceso a servicios de salud |
| `NoDocbcCost` | Limitación por costos médicos |
| `Education` | Nivel educativo |
| `Income` | Nivel de ingresos |

### ⚙️ Parámetros de entrenamiento (ambos modelos)

```
iterations    = 500
depth         = 6
learning_rate = 0.05
loss_function = Logloss
eval_metric   = AUC
random_seed   = 42
```

---

## 🧩 Motor Experto: EYRA

EYRA es el módulo de interpretación que combina las probabilidades de los modelos con las **importancias reales de cada variable** (`get_feature_importance()` de CatBoost) para producir tres tipos de salida:

### 1. 📊 Análisis (`getAnalisis`)
Resumen ejecutivo que menciona los factores de riesgo activos ordenados por su peso estadístico real, junto con los porcentajes de riesgo clínico y conductual.

### 2. 💡 Explicaciones (`getExplicaciones`)
Mensajes personalizados que explican **por qué** el resultado fue el que fue, clasificados por nivel de urgencia:

- 🚨 **Crítico** — Valores fuera de rango diagnóstico
- ⚠️ **Moderado** — Valores en zona de prediabetes o riesgo intermedio
- ℹ️ **Informativo** — Factores de menor peso pero relevantes

### 3. 📋 Recomendaciones (`getRecomendaciones`)
Acciones concretas y alcanzables, también priorizadas por urgencia:

- 🔴⏰ **Urgente** — Requieren atención médica pronta
- 🟠📌 **Importantes** — Cambios de hábito recomendados
- 🟢📝 **Preventivas** — Mantenimiento del estado actual de salud

---

## 📡 API REST

La API está construida con **Flask** y expone los siguientes endpoints:

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/clinic` | Predicción clínica (% de riesgo) |
| `POST` | `/api/conductual` | Predicción conductual (% de riesgo) |
| `POST` | `/api/metricas` | Métricas para gráfica de radar |
| `POST` | `/api/eyra` | Análisis EYRA completo |

### Ejemplo de payload para `/api/eyra`

```json
{
  "clinico": {
    "edad": 52,
    "imc": 28.5,
    "glu_suero": 110,
    "hb1ac": 5.9,
    "insulina": null,
    "trig": 170,
    "col_hdl": 38,
    "col_ldl": 130,
    "ac_urico": null,
    "HighBP": 1,
    "Sex": 1
  },
  "conductual": {
    "PhysActivity": 0,
    "Smoker": 0,
    "Fruits": 1,
    "BMI": 28.5,
    "Age": 52,
    "Veggies": 0,
    "HvyAlcoholConsump": 0,
    "DiffWalk": 0,
    "MentHlth": 5,
    "AnyHealthcare": 1,
    "NoDocbcCost": 0,
    "Education": 4,
    "Income": 3
  }
}
```

### Ejemplo de respuesta de `/api/eyra`

```json
{
  "eyra_result": {
    "analisis": "Al realizar el análisis de la predicción Clínica y Conductual nos dimos cuenta que Glucosa en ayunas, Triglicéridos y Presión arterial alta fueron los factores que causan que se tenga 63.4% en su riesgo Clínico y 48.2% en su riesgo Conductual.",
    "explicaciones": [
      "⚠️ Tu azúcar en ayunas (110 mg/dL) o tu promedio de glucosa (5.9%) salieron un poco elevados. Esto indica prediabetes, pero estás muy a tiempo de corregirlo (Este factor influye: 18.3%).",
      "⚠️ Tus triglicéridos (170 mg/dL) están por encima del límite recomendado...",
      "ℹ️ Hacer poca actividad física impide que tus músculos quemen el azúcar de la comida como energía..."
    ],
    "recomendaciones": [
      "🟠📌 Estás en el momento perfecto para actuar (Prediabetes). Con solo bajar el consumo de refrescos, jugos, harinas refinadas y pan dulce, tus niveles pueden volver a la normalidad.",
      "🟠📌 Sigue la meta recomendada: intenta acumular al menos 2 horas y media de ejercicio a la semana..."
    ]
  }
}
```

---

## 📈 Métricas del Modelo

El entrenamiento del modelo conductual alcanzó una **pérdida logarítmica (Logloss) de 0.5312** después de 500 iteraciones, partiendo de 0.6795 en la iteración 0, lo que representa una reducción del ~21.8% en el error de clasificación a lo largo del entrenamiento.

```
Iteración   0  →  Logloss: 0.6795
Iteración 100  →  Logloss: 0.5416
Iteración 250  →  Logloss: 0.5369
Iteración 499  →  Logloss: 0.5312  ✅
```

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/ExpertSystem_GlucoPredict-AI.git
cd ExpertSystem_GlucoPredict-AI
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

### 3. Entrenar los modelos (primera vez)

```bash
# Modelo clínico
python IA/sistema_experto/modelSClinic.py

# Modelo conductual
python IA/sistema_experto/modelSConductual.py
```

> Los modelos se guardarán como `clinicModel.cbm` y `conductualModel.cbm` dentro de `IA/sistema_experto/`.

### 4. Iniciar la API

```bash
# Desarrollo
flask --app IA/api/app.py run

# Producción con Gunicorn
gunicorn "IA.api.app:app"
```

---

## 🧪 Dependencias principales

| Librería | Versión | Uso |
|---|---|---|
| Flask | 3.1.3 | API REST |
| flask-cors | 6.0.5 | Soporte CORS |
| CatBoost | 1.2.10 | Modelos de predicción |
| scikit-learn | 1.9.0 | División de datos y validación |
| pandas | 3.0.3 | Manejo de datos |
| numpy | 2.4.6 | Operaciones numéricas |
| gunicorn | 26.0.0 | Servidor de producción |

---

## 🌐 Despliegue

El proyecto está configurado para desplegarse en **Render** usando `gunicorn` como servidor WSGI. El archivo `requirements.txt` incluye todas las dependencias necesarias para el entorno de producción.

---

## ⚠️ Aviso importante

> GlucoPredict-AI es una **herramienta de apoyo y orientación** basada en inteligencia artificial. Sus resultados **no reemplazan el diagnóstico médico profesional**. Ante cualquier hallazgo de riesgo, se recomienda siempre consultar a un médico certificado.

---

## 📄 Licencia

Este proyecto se distribuye bajo los términos definidos por el equipo de desarrollo. Consulta el archivo `LICENSE` para más información.

---

<div align="center">
  <sub>Desarrollado con ❤️ para mejorar la salud preventiva en México</sub>
</div>