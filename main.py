from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
import joblib
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load models
breast_cancer_model = joblib.load("breast_cancer_model.pkl")
diabetes_model = joblib.load("diabetes_model.pkl")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/input", response_class=HTMLResponse)
async def get_input(request: Request):
    return templates.TemplateResponse("input.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    disease: str = Form(...),
    **form_data
):
    if disease == "Breast Cancer":
        features = [
            float(form_data.get(f"feature_{i}")) for i in range(30)
        ]
        prediction = breast_cancer_model.predict([features])[0]
        result = "Malignant" if prediction == 0 else "Benign"
        return templates.TemplateResponse("result_cancer.html", {"request": request, "result": result})
    elif disease == "Diabetes":
        features = [
            float(form_data.get(f"feature_{i}")) for i in range(8)
        ]
        prediction = diabetes_model.predict([features])[0]
        result = "Diabetic" if prediction == 1 else "Non-Diabetic"
        return templates.TemplateResponse("result_diabetes.html", {"request": request, "result": result})
    else:
        return HTMLResponse(content="Invalid disease", status_code=400)
