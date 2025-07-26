from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib
import numpy as np

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

cancer_model = joblib.load("models/cancer_model.pkl")
diabetes_model = joblib.load("models/diabetes_model.pkl")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/input", response_class=HTMLResponse)
def get_input(request: Request):
    return templates.TemplateResponse("input.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, disease: str = Form(...), **data):
    features = list(map(float, data.values()))

    if disease == "Breast Cancer":
        prediction = cancer_model.predict([features])[0]
        confidence = np.max(cancer_model.predict_proba([features])) * 100
        result = "Malignant" if prediction == 1 else "Benign"
        return templates.TemplateResponse("result_cancer.html", {
            "request": request,
            "result": result,
            "confidence": f"{confidence:.2f}%"
        })

    elif disease == "Diabetes":
        prediction = diabetes_model.predict([features])[0]
        result = "Positive" if prediction == 1 else "Negative"
        return templates.TemplateResponse("result_diabetes.html", {
            "request": request,
            "result": result
        })

    return templates.TemplateResponse("index.html", {"request": request, "error": "Invalid input"})
