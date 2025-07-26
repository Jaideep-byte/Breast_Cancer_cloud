from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
import pickle

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load models
breast_cancer_model = pickle.load(open("breast_cancer_model.pkl", "rb"))
diabetes_model = pickle.load(open("diabetes_model.pkl", "rb"))

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/input", response_class=HTMLResponse)
async def input_page(request: Request):
    return templates.TemplateResponse("input.html", {"request": request})

@app.post("/predict_diabetes", response_class=HTMLResponse)
async def predict_diabetes(
    request: Request,
    pregnancies: float = Form(...),
    glucose: float = Form(...),
    blood_pressure: float = Form(...),
    skin_thickness: float = Form(...),
    insulin: float = Form(...),
    bmi: float = Form(...),
    diabetes_pedigree_function: float = Form(...),
    age: float = Form(...)
):
    data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness,
                      insulin, bmi, diabetes_pedigree_function, age]])
    prediction = diabetes_model.predict(data)[0]
    confidence = max(diabetes_model.predict_proba(data)[0])
    result = "Diabetic" if prediction == 1 else "Not Diabetic"
    return templates.TemplateResponse("result_diabetes.html", {
        "request": request,
        "result": result,
        "confidence": round(confidence * 100, 2)
    })

@app.post("/predict_cancer", response_class=HTMLResponse)
async def predict_cancer(
    request: Request,
    radius_mean: float = Form(...),
    texture_mean: float = Form(...),
    perimeter_mean: float = Form(...),
    area_mean: float = Form(...),
    smoothness_mean: float = Form(...),
    compactness_mean: float = Form(...),
    concavity_mean: float = Form(...),
    concave_points_mean: float = Form(...),
    symmetry_mean: float = Form(...),
    fractal_dimension_mean: float = Form(...),
    radius_se: float = Form(...),
    texture_se: float = Form(...),
    perimeter_se: float = Form(...),
    area_se: float = Form(...),
    smoothness_se: float = Form(...),
    compactness_se: float = Form(...),
    concavity_se: float = Form(...),
    concave_points_se: float = Form(...),
    symmetry_se: float = Form(...),
    fractal_dimension_se: float = Form(...),
    radius_worst: float = Form(...),
    texture_worst: float = Form(...),
    perimeter_worst: float = Form(...),
    area_worst: float = Form(...),
    smoothness_worst: float = Form(...),
    compactness_worst: float = Form(...),
    concavity_worst: float = Form(...),
    concave_points_worst: float = Form(...),
    symmetry_worst: float = Form(...),
    fractal_dimension_worst: float = Form(...)
):
    features = [
        radius_mean, texture_mean, perimeter_mean, area_mean, smoothness_mean,
        compactness_mean, concavity_mean, concave_points_mean, symmetry_mean, fractal_dimension_mean,
        radius_se, texture_se, perimeter_se, area_se, smoothness_se,
        compactness_se, concavity_se, concave_points_se, symmetry_se, fractal_dimension_se,
        radius_worst, texture_worst, perimeter_worst, area_worst, smoothness_worst,
        compactness_worst, concavity_worst, concave_points_worst, symmetry_worst, fractal_dimension_worst
    ]
    input_data = np.array([features])
    prediction = breast_cancer_model.predict(input_data)[0]
    confidence = max(breast_cancer_model.predict_proba(input_data)[0])
    result = "Malignant" if prediction == 0 else "Benign"
    return templates.TemplateResponse("result_cancer.html", {
        "request": request,
        "result": result,
        "confidence": round(confidence * 100, 2)
    })
