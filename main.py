from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import numpy as np
import pickle

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

with open("breast_cancer_model.pkl", "rb") as f:
    cancer_model = pickle.load(f)

with open("diabetes_model.pkl", "rb") as f:
    diabetes_model = pickle.load(f)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, disease: str = Form(...), **kwargs):
    try:
        input_values = list(map(float, kwargs.values()))
        features = np.array(input_values).reshape(1, -1)
        if disease == "cancer":
            prediction = cancer_model.predict(features)[0]
            confidence = cancer_model.predict_proba(features)[0][prediction]
            return templates.TemplateResponse("result_cancer.html", {
                "request": request,
                "result": "Malignant" if prediction == 0 else "Benign",
                "confidence": round(confidence * 100, 2)
            })
        elif disease == "diabetes":
            prediction = diabetes_model.predict(features)[0]
            return templates.TemplateResponse("result_diabetes.html", {
                "request": request,
                "result": "Positive" if prediction == 1 else "Negative"
            })
    except Exception as e:
        return HTMLResponse(content=f"<h3>Error: {str(e)}</h3>")
