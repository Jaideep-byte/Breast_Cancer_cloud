from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import numpy as np
import joblib

app = FastAPI()

# Mount static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load ML models
cancer_model = joblib.load("models/breast_cancer_model.pkl")
diabetes_model = joblib.load("models/diabetes_model.pkl")

# Input format
class InputFeatures(BaseModel):
    features: list[float]

# API Route: Breast Cancer Prediction
@app.post("/predict_cancer")
def predict_cancer(data: InputFeatures):
    features = np.array(data.features).reshape(1, -1)
    prediction = cancer_model.predict(features)[0]
    proba = cancer_model.predict_proba(features)[0]

    result = {
        "prediction": "Malignant" if prediction == 1 else "Benign",
        "Benign": round(float(proba[0]), 4),
        "Malignant": round(float(proba[1]), 4)
    }
    return result

# API Route: Diabetes Prediction
@app.post("/predict_diabetes")
def predict_diabetes(data: InputFeatures):
    features = np.array(data.features).reshape(1, -1)
    prediction = diabetes_model.predict(features)[0]
    proba = diabetes_model.predict_proba(features)[0]

    result = {
        "prediction": "Diabetic" if prediction == 1 else "Non-Diabetic",
        "Diabetic": round(float(proba[1]), 4),
        "Non_Diabetic": round(float(proba[0]), 4)
    }
    return result

# Frontend: Home Page
@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Frontend: Input Page
@app.get("/input", response_class=HTMLResponse)
def read_input(request: Request):
    return templates.TemplateResponse("input.html", {"request": request})

# Frontend: Cancer Result Page
@app.get("/result_cancer", response_class=HTMLResponse)
def result_cancer(request: Request, prediction: str, Benign: float = 0.0, Malignant: float = 0.0):
    return templates.TemplateResponse("result_cancer.html", {
        "request": request,
        "prediction": prediction,
        "confidence": {
            "Benign": Benign,
            "Malignant": Malignant
        }
    })

# Frontend: Diabetes Result Page
@app.get("/result_diabetes", response_class=HTMLResponse)
def result_diabetes(request: Request, prediction: str, Diabetic: float = 0.0, Non_Diabetic: float = 0.0):
    return templates.TemplateResponse("result_diabetes.html", {
        "request": request,
        "prediction": prediction,
        "confidence": {
            "Diabetic": Diabetic,
            "Non-Diabetic": Non_Diabetic
        }
    })
# Frontend: Landing Page
@app.get("/landing", response_class=HTMLResponse)
def landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")