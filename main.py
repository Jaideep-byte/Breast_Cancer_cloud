from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib
import os

app = FastAPI()

# Mount static and template directories
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load models
cancer_model = joblib.load("breast_cancer_model.pkl")
diabetes_model = joblib.load("diabetes_model.pkl")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, disease: str = Form(...), **kwargs):
    if disease == "diabetes":
        try:
            input_data = [
                float(kwargs['Pregnancies']),
                float(kwargs['Glucose']),
                float(kwargs['BloodPressure']),
                float(kwargs['SkinThickness']),
                float(kwargs['Insulin']),
                float(kwargs['BMI']),
                float(kwargs['DiabetesPedigreeFunction']),
                float(kwargs['Age'])
            ]
        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Missing input: {e}")

        prediction = diabetes_model.predict([input_data])[0]
        confidence = diabetes_model.predict_proba([input_data])[0][prediction]

        result = "Positive for Diabetes" if prediction == 1 else "Negative for Diabetes"
        return templates.TemplateResponse("result_diabetes.html", {
            "request": request,
            "result": result,
            "confidence": f"{confidence * 100:.2f}%"
        })

    elif disease == "cancer":
        try:
            input_data = [float(kwargs[f"feature{i+1}"]) for i in range(30)]
        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Missing input: {e}")

        prediction = cancer_model.predict([input_data])[0]
        confidence = cancer_model.predict_proba([input_data])[0][prediction]

        result = "Malignant (Cancerous)" if prediction == 1 else "Benign (Non-Cancerous)"
        return templates.TemplateResponse("result_cancer.html", {
            "request": request,
            "result": result,
            "confidence": f"{confidence * 100:.2f}%"
        })

    else:
        raise HTTPException(status_code=400, detail="Invalid disease type")
