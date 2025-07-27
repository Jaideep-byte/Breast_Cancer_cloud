from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import joblib
import numpy as np

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load models
breast_cancer_model = joblib.load("breast_cancer_model.pkl")
diabetes_model = joblib.load("diabetes_model.pkl")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/input", response_class=HTMLResponse)
async def input_page(request: Request):
    return templates.TemplateResponse("input.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, disease: str = Form(...), **kwargs):
    try:
        features = list(map(float, kwargs.values()))
        if disease == "cancer":
            pred_proba = breast_cancer_model.predict_proba([features])[0]
            pred = breast_cancer_model.predict([features])[0]
            result = "Malignant" if pred == 0 else "Benign"
            confidence = round(max(pred_proba) * 100, 2)
            return templates.TemplateResponse("result_cancer.html", {
                "request": request, "result": result, "confidence": confidence
            })
        elif disease == "diabetes":
            pred_proba = diabetes_model.predict_proba([features])[0]
            pred = diabetes_model.predict([features])[0]
            result = "Diabetic" if pred == 1 else "Not Diabetic"
            confidence = round(max(pred_proba) * 100, 2)
            return templates.TemplateResponse("result_diabetes.html", {
                "request": request, "result": result, "confidence": confidence
            })
        else:
            return {"error": "Invalid disease selected"}
    except Exception as e:
        return {"error": str(e)}
