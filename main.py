from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import joblib
import numpy as np
from pathlib import Path

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load models
model_bc = joblib.load("breast_cancer_model.pkl")
model_db = joblib.load("diabetes_model.pkl")

# Feature counts
features_bc = [
    'Radius Mean', 'Texture Mean', 'Perimeter Mean', 'Area Mean', 'Smoothness Mean',
    'Compactness Mean', 'Concavity Mean', 'Concave Points Mean', 'Symmetry Mean', 'Fractal Dimension Mean',
    'Radius SE', 'Texture SE', 'Perimeter SE', 'Area SE', 'Smoothness SE',
    'Compactness SE', 'Concavity SE', 'Concave Points SE', 'Symmetry SE', 'Fractal Dimension SE',
    'Radius Worst', 'Texture Worst', 'Perimeter Worst', 'Area Worst', 'Smoothness Worst',
    'Compactness Worst', 'Concavity Worst', 'Concave Points Worst', 'Symmetry Worst', 'Fractal Dimension Worst'
]

features_db = [
    'Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness', 'Insulin',
    'BMI', 'Diabetes Pedigree Function', 'Age'
]

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/input", response_class=HTMLResponse)
def input_page(request: Request):
    return templates.TemplateResponse("input.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    disease: str = Form(...),
    **kwargs
):
    if disease == "cancer":
        features = [float(kwargs.get(f"feature_{i}", 0)) for i in range(30)]
        prediction = model_bc.predict([features])[0]
        confidence = round(np.max(model_bc.predict_proba([features])) * 100, 2)
        result = "Malignant" if prediction == 0 else "Benign"
        return templates.TemplateResponse("result_cancer.html", {
            "request": request,
            "result": result,
            "confidence": confidence
        })

    elif disease == "diabetes":
        features = [float(kwargs.get(f"feature_{i}", 0)) for i in range(8)]
        prediction = model_db.predict([features])[0]
        confidence = round(np.max(model_db.predict_proba([features])) * 100, 2)
        result = "Diabetic" if prediction == 1 else "Non-Diabetic"
        return templates.TemplateResponse("result_diabetes.html", {
            "request": request,
            "result": result,
            "confidence": confidence
        })

    return {"error": "Invalid disease type"}
