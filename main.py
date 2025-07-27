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
cancer_model = joblib.load("breast_cancer_model.pkl")
diabetes_model = joblib.load("diabetes_model.pkl")

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, disease: str = Form(...), **kwargs):
    if disease == "cancer":
        values = [float(kwargs[f"feature{i}"]) for i in range(30)]
        result = cancer_model.predict([values])[0]
        pred_text = "Malignant" if result == 0 else "Benign"
        return templates.TemplateResponse("result_cancer.html", {
            "request": request, "prediction": pred_text
        })
    elif disease == "diabetes":
        features = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
                    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
        values = [float(kwargs[feature]) for feature in features]
        result = diabetes_model.predict([values])[0]
        pred_text = "Diabetic" if result == 1 else "Non-Diabetic"
        return templates.TemplateResponse("result_diabetes.html", {
            "request": request, "prediction": pred_text
        })
