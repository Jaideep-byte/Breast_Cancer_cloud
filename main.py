from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
import joblib

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load models
breast_cancer_model = joblib.load("breast_cancer_model.pkl")
diabetes_model = joblib.load("diabetes_model.pkl")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/input", response_class=HTMLResponse)
async def input_form(request: Request, disease: str):
    return templates.TemplateResponse("input.html", {"request": request, "disease": disease})

@app.post("/predict_cancer", response_class=HTMLResponse)
async def predict_cancer(request: Request, **kwargs):
    features = [float(value) for value in kwargs.values()]
    prediction = breast_cancer_model.predict([features])[0]
    result = "Malignant" if prediction == 0 else "Benign"
    return templates.TemplateResponse("result_cancer.html", {"request": request, "result": result})

@app.post("/predict_diabetes", response_class=HTMLResponse)
async def predict_diabetes(request: Request, **kwargs):
    features = [float(value) for value in kwargs.values()]
    prediction = diabetes_model.predict([features])[0]
    result = "Diabetic" if prediction == 1 else "Non-Diabetic"
    return templates.TemplateResponse("result_diabetes.html", {"request": request, "result": result})
