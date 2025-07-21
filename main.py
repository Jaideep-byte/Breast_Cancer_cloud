#!/usr/bin/env python
# coding: utf-8

# In[3]:


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
from typing import List
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load model
try:
    model = joblib.load("breast_cancer_model.pkl")
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    raise RuntimeError("Model could not be loaded.")

# Initialize app
app = FastAPI(title="Breast Cancer Predictor API", version="1.0")

# Input schema
class CancerFeatures(BaseModel):
    features: List[float] = Field(
        ...,
        example=[
            14.2, 20.7, 92.0, 633.0, 0.09, 0.19, 0.2, 0.07, 0.18, 0.06,
            0.4, 1.0, 3.0, 40.0, 0.006, 0.05, 0.06, 0.02, 0.02, 0.006,
            16.0, 28.0, 110.0, 800.0, 0.1, 0.4, 0.5, 0.15, 0.3, 0.07
        ],
        min_items=30,
        max_items=30
    )

class CancerBatch(BaseModel):
    records: List[CancerFeatures]

# Root endpoint
@app.get("/")
def home():
    return {"message": "Breast Cancer Prediction API is up and running!"}

# Single prediction endpoint
@app.post("/predict")
def predict(data: CancerFeatures):
    if len(data.features) != 30:
        raise HTTPException(status_code=400, detail="Exactly 30 features are required.")

    input_data = np.array(data.features).reshape(1, -1)
    prediction = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0]

    result = {
        "prediction": "Benign" if prediction == 1 else "Malignant",
        "confidence": {
            "Benign": round(proba[1], 4),
            "Malignant": round(proba[0], 4)
        }
    }

    logging.info(f"Prediction made: {result}")
    return result

# Batch prediction endpoint
@app.post("/batch_predict")
def batch_predict(data: CancerBatch):
    all_features = [record.features for record in data.records]

    for i, features in enumerate(all_features):
        if len(features) != 30:
            raise HTTPException(status_code=400, detail=f"Record {i+1} does not contain 30 features.")

    input_data = np.array(all_features)
    predictions = model.predict(input_data)
    probas = model.predict_proba(input_data)

    results = []
    for i in range(len(predictions)):
        results.append({
            "prediction": "Benign" if predictions[i] == 1 else "Malignant",
            "confidence": {
                "Benign": round(probas[i][1], 4),
                "Malignant": round(probas[i][0], 4)
            }
        })

    logging.info(f"Batch prediction complete. {len(results)} records processed.")
    return {"results": results}

