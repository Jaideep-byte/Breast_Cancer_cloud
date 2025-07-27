from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib
import numpy as np

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load models
cancer_model = joblib.load("breast_cancer_model.pkl")
diabetes_model = joblib.load("diabetes_model.pkl")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/input", response_class=HTMLResponse)
async def input_form(request: Request):
    return templates.TemplateResponse("input.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, disease: str = Form(...), **kwargs):
    if disease == "cancer":
        features = [float(kwargs.get(f"feature{i}")) for i in range(1, 31)]
        prediction = cancer_model.predict([features])[0]
        return templates.TemplateResponse("result_cancer.html", {
            "request": request,
            "prediction": "Malignant" if prediction == 0 else "Benign"
        })
    elif disease == "diabetes":
        features = [float(kwargs.get(f"feature{i}")) for i in range(1, 9)]
        prediction = diabetes_model.predict([features])[0]
        return templates.TemplateResponse("result_diabetes.html", {
            "request": request,
            "prediction": "Diabetic" if prediction == 1 else "Non-Diabetic"
        })
    else:
        return {"detail": "Invalid disease selected"}
