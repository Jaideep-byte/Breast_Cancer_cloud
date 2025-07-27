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
        # Convert all form values to float (excluding 'disease')
        features = [float(value) for key, value in kwargs.items()]

        if disease == "cancer":
            pred = breast_cancer_model.predict([features])[0]
            prob = breast_cancer_model.predict_proba([features])[0]
            result = "Malignant" if pred == 0 else "Benign"
            confidence = round(max(prob) * 100, 2)
            return templates.TemplateResponse("result_cancer.html", {
                "request": request,
                "result": result,
                "confidence": confidence
            })

        elif disease == "diabetes":
            pred = diabetes_model.predict([features])[0]
            prob = diabetes_model.predict_proba([features])[0]
            result = "Diabetic" if pred == 1 else "Not Diabetic"
            confidence = round(max(prob) * 100, 2)
            return templates.TemplateResponse("result_diabetes.html", {
                "request": request,
                "result": result,
                "confidence": confidence
            })
        else:
            return templates.TemplateResponse("input.html", {"request": request, "error": "Invalid disease selected."})

    except Exception as e:
        return templates.TemplateResponse("input.html", {"request": request, "error": str(e)})
