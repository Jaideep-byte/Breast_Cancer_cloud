# main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

models = {
    "Breast Cancer": joblib.load("models/breast_cancer_model.pkl"),
    "Diabetes": joblib.load("models/diabetes_model.pkl")
}

features = {
    "Breast Cancer": [
        "Radius Mean", "Texture Mean", "Perimeter Mean", "Area Mean", "Smoothness Mean",
        "Compactness Mean", "Concavity Mean", "Concave Points Mean", "Symmetry Mean", "Fractal Dimension Mean",
        "Radius SE", "Texture SE", "Perimeter SE", "Area SE", "Smoothness SE",
        "Compactness SE", "Concavity SE", "Concave Points SE", "Symmetry SE", "Fractal Dimension SE",
        "Radius Worst", "Texture Worst", "Perimeter Worst", "Area Worst", "Smoothness Worst",
        "Compactness Worst", "Concavity Worst", "Concave Points Worst", "Symmetry Worst", "Fractal Dimension Worst"
    ],
    "Diabetes": [
        "Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness", "Insulin",
        "BMI", "Diabetes Pedigree Function", "Age"
    ]
}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/input", response_class=HTMLResponse)
async def input_form(request: Request):
    return templates.TemplateResponse("input.html", {"request": request, "features": features})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, disease: str = Form(...), feature_values: str = Form(...)):
    try:
        model = models[disease]
        input_values = [float(x) for x in feature_values.split(",")]
        prediction = model.predict([input_values])[0]
        result = "Positive" if prediction == 1 else "Negative"
        return templates.TemplateResponse("result.html", {
            "request": request,
            "disease": disease,
            "result": result
        })
    except Exception as e:
        return templates.TemplateResponse("result.html", {
            "request": request,
            "disease": disease,
            "result": f"Error: {str(e)}"
        })