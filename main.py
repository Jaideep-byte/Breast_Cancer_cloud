from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import joblib

app = FastAPI()

# Load models
breast_cancer_model = joblib.load("breast_cancer_model.pkl")
diabetes_model = joblib.load("diabetes_model.pkl")

# Mount static and template files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/input", response_class=HTMLResponse)
def input_page(request: Request):
    return templates.TemplateResponse("input.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, disease: str = Form(...)):
    form_data = await request.form()
    
    features = []
    for key, value in form_data.items():
        if key != "disease":
            try:
                features.append(float(value))
            except ValueError:
                features.append(0.0)  # fallback if input is bad

    if disease == "cancer":
        prediction = breast_cancer_model.predict([features])[0]
        result = "Malignant" if prediction == 1 else "Benign"
        image_path = "/static/syringe.png"
        return templates.TemplateResponse("result_cancer.html", {
            "request": request,
            "result": result,
            "image_path": image_path
        })

    elif disease == "diabetes":
        prediction = diabetes_model.predict([features])[0]
        result = "Positive for Diabetes" if prediction == 1 else "Negative for Diabetes"
        image_path = "/static/sugar.png"
        return templates.TemplateResponse("result_diabetes.html", {
            "request": request,
            "result": result,
            "image_path": image_path
        })

    return templates.TemplateResponse("index.html", {"request": request})
