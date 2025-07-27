from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import joblib
import numpy as np
from pathlib import Path

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load models
model_cancer = joblib.load("breast_cancer_model.pkl")
model_diabetes = joblib.load("diabetes_model.pkl")

# Feature names
cancer_features = [
    "Radius Mean", "Texture Mean", "Perimeter Mean", "Area Mean", "Smoothness Mean",
    "Compactness Mean", "Concavity Mean", "Concave Points Mean", "Symmetry Mean", "Fractal Dimension Mean",
    "Radius SE", "Texture SE", "Perimeter SE", "Area SE", "Smoothness SE",
    "Compactness SE", "Concavity SE", "Concave Points SE", "Symmetry SE", "Fractal Dimension SE",
    "Radius Worst", "Texture Worst", "Perimeter Worst", "Area Worst", "Smoothness Worst",
    "Compactness Worst", "Concavity Worst", "Concave Points Worst", "Symmetry Worst", "Fractal Dimension Worst"
]

diabetes_features = [
    "Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness",
    "Insulin", "BMI", "Diabetes Pedigree Function", "Age"
]

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/input", response_class=HTMLResponse)
def input_form(request: Request):
    return templates.TemplateResponse("input.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    disease: str = Form(...),
    **kwargs
):
    # Convert values to float
    try:
        features = [float(v) for v in kwargs.values()]
    except:
        return HTMLResponse(content="Invalid input data", status_code=400)

    features_array = np.array(features).reshape(1, -1)

    if disease == "cancer":
        prediction = model_cancer.predict(features_array)[0]
        confidence = model_cancer.predict_proba(features_array).max()
        result = "Malignant" if prediction == 0 else "Benign"
        return templates.TemplateResponse("result_cancer.html", {
            "request": request,
            "result": result,
            "confidence": round(confidence * 100, 2)
        })
    elif disease == "diabetes":
        prediction = model_diabetes.predict(features_array)[0]
        confidence = model_diabetes.predict_proba(features_array).max()
        result = "Diabetic" if prediction == 1 else "Non-Diabetic"
        return templates.TemplateResponse("result_diabetes.html", {
            "request": request,
            "result": result,
            "confidence": round(confidence * 100, 2)
        })
    else:
        return HTMLResponse(content="Invalid disease selection", status_code=400)
