from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib
import numpy as np

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load models
cancer_model = joblib.load("breast_cancer_model.pkl")
diabetes_model = joblib.load("diabetes_model.pkl")

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
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
]

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, disease: str = Form(...), **kwargs):
    # Convert input values to float
    input_values = [float(val) for val in kwargs.values()]

    if disease == "cancer":
        prediction = cancer_model.predict([input_values])[0]
        prob = cancer_model.predict_proba([input_values])[0]
        confidence = round(max(prob) * 100, 2)
        result = "Malignant" if prediction == 0 else "Benign"
        return templates.TemplateResponse("result_cancer.html", {
            "request": request,
            "result": result,
            "confidence": confidence
        })

    elif disease == "diabetes":
        prediction = diabetes_model.predict([input_values])[0]
        prob = diabetes_model.predict_proba([input_values])[0]
        confidence = round(max(prob) * 100, 2)
        result = "Diabetic" if prediction == 1 else "Non-Diabetic"
        return templates.TemplateResponse("result_diabetes.html", {
            "request": request,
            "result": result,
            "confidence": confidence
        })

    else:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Invalid disease selected"
        })
