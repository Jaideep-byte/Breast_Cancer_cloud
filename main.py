from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
import joblib

# Initialize FastAPI app
app = FastAPI()

# Set up templates and static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load models
breast_cancer_model = joblib.load("breast_cancer_model.pkl")
diabetes_model = joblib.load("diabetes_model.pkl")

# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Input form page
@app.get("/input", response_class=HTMLResponse)
async def input_page(request: Request):
    return templates.TemplateResponse("input.html", {"request": request})

# Prediction handler
@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request):
    form = await request.form()
    disease = form.get("disease")

    # Collect all feature values
    features = []
    for key in sorted(form.keys()):
        if key.startswith("feature"):
            try:
                features.append(float(form[key]))
            except:
                features.append(0.0)

    input_data = np.array([features])

    # Breast Cancer Prediction
    if disease == "cancer":
        prediction = breast_cancer_model.predict(input_data)[0]
        confidence = round(np.max(breast_cancer_model.predict_proba(input_data)) * 100, 2)
        result = "Malignant" if prediction == 1 else "Benign"
        return templates.TemplateResponse("result_cancer.html", {
            "request": request,
            "result": result,
            "confidence": confidence
        })

    # Diabetes Prediction
    elif disease == "diabetes":
        prediction = diabetes_model.predict(input_data)[0]
        confidence = round(np.max(diabetes_model.predict_proba(input_data)) * 100, 2)
        result = "Diabetic" if prediction == 1 else "Not Diabetic"
        return templates.TemplateResponse("result_diabetes.html", {
            "request": request,
            "result": result,
            "confidence": confidence
        })

    # Invalid disease selected
    else:
        return templates.TemplateResponse("input.html", {
            "request": request,
            "error": "Please select a valid disease."
        })
