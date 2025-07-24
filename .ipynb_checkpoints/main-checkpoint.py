from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
from typing import List
import logging
import os

# ================= Setup Logging =================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ================= Load Models =================
try:
    cancer_model = joblib.load("models/breast_cancer_model.pkl")
    logging.info("✅ Breast cancer model loaded successfully.")
except Exception as e:
    logging.error(f"❌ Error loading breast cancer model: {e}")
    raise RuntimeError("Breast cancer model could not be loaded.")

try:
    diabetes_model = joblib.load("models/diabetes_model.pkl")
    logging.info("✅ Diabetes model loaded successfully.")
except Exception as e:
    logging.error(f"❌ Error loading diabetes model: {e}")
    raise RuntimeError("Diabetes model could not be loaded.")

# ================= Initialize App =================
app = FastAPI(
    title="Disease Prediction API",
    version="2.0",
    description="API to predict Breast Cancer and Diabetes using ML models"
)

# ================= Input Schemas =================
class CancerFeatures(BaseModel):
    features: List[float] = Field(
        ..., min_items=30, max_items=30,
        example=[14.2, 20.7, 92.0, 633.0, 0.09, 0.19, 0.2, 0.07, 0.18, 0.06,
                 0.4, 1.0, 3.0, 40.0, 0.006, 0.05, 0.06, 0.02, 0.02, 0.006,
                 16.0, 28.0, 110.0, 800.0, 0.1, 0.4, 0.5, 0.15, 0.3, 0.07]
    )

class CancerBatch(BaseModel):
    records: List[CancerFeatures]

class DiabetesFeatures(BaseModel):
    features: List[float] = Field(
        ..., min_items=8, max_items=8,
        example=[2, 120, 70, 27, 85, 30.5, 0.3, 25]
    )

class DiabetesBatch(BaseModel):
    records: List[DiabetesFeatures]

# ================= Root Endpoint =================
@app.get("/")
def home():
    return {
        "message": "🚀 Disease Prediction API is running!",
        "available_endpoints": [
            "/predict_cancer",
            "/batch_predict_cancer",
            "/predict_diabetes",
            "/batch_predict_diabetes"
        ]
    }

# ================= Cancer Endpoints =================
@app.post("/predict_cancer")
def predict_cancer(data: CancerFeatures):
    input_data = np.array(data.features).reshape(1, -1)
    prediction = cancer_model.predict(input_data)[0]
    proba = cancer_model.predict_proba(input_data)[0]

    result = {
        "prediction": "Benign" if prediction == 1 else "Malignant",
        "confidence": {
            "Benign": round(proba[1], 4),
            "Malignant": round(proba[0], 4)
        }
    }

    logging.info(f"Breast cancer prediction: {result}")
    return result

@app.post("/batch_predict_cancer")
def batch_predict_cancer(data: CancerBatch):
    inputs = [record.features for record in data.records]
    input_data = np.array(inputs)
    predictions = cancer_model.predict(input_data)
    probas = cancer_model.predict_proba(input_data)

    results = []
    for i in range(len(predictions)):
        results.append({
            "prediction": "Benign" if predictions[i] == 1 else "Malignant",
            "confidence": {
                "Benign": round(probas[i][1], 4),
                "Malignant": round(probas[i][0], 4)
            }
        })

    logging.info(f"Batch cancer prediction done: {len(results)} records")
    return {"results": results}

# ================= Diabetes Endpoints =================
@app.post("/predict_diabetes")
def predict_diabetes(data: DiabetesFeatures):
    input_data = np.array(data.features).reshape(1, -1)
    prediction = diabetes_model.predict(input_data)[0]
    proba = diabetes_model.predict_proba(input_data)[0]

    result = {
        "prediction": "Diabetic" if prediction == 1 else "Non-Diabetic",
        "confidence": {
            "Diabetic": round(proba[1], 4),
            "Non-Diabetic": round(proba[0], 4)
        }
    }

    logging.info(f"Diabetes prediction: {result}")
    return result

@app.post("/batch_predict_diabetes")
def batch_predict_diabetes(data: DiabetesBatch):
    inputs = [record.features for record in data.records]
    input_data = np.array(inputs)
    predictions = diabetes_model.predict(input_data)
    probas = diabetes_model.predict_proba(input_data)

    results = []
    for i in range(len(predictions)):
        results.append({
            "prediction": "Diabetic" if predictions[i] == 1 else "Non-Diabetic",
            "confidence": {
                "Diabetic": round(probas[i][1], 4),
                "Non-Diabetic": round(probas[i][0], 4)
            }
        })

    logging.info(f"Batch diabetes prediction done: {len(results)} records")
    return {"results": results}
