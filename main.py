from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load models
breast_cancer_model = joblib.load("breast_cancer_model.pkl")
diabetes_model = joblib.load("diabetes_model.pkl")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/input", response_class=HTMLResponse)
def show_input_page(request: Request):
    return templates.TemplateResponse("input.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    disease: str = Form(...),
    **kwargs: str
):
    if disease == "cancer":
        input_features = [float(kwargs[f"feature_{i}"]) for i in range(1, 31)]
        prediction = breast_cancer_model.predict([input_features])[0]
        result = "Malignant" if prediction == 0 else "Benign"
        return templates.TemplateResponse("result_cancer.html", {"request": request, "result": result})
    
    elif disease == "diabetes":
        features = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
                    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
        input_features = [float(kwargs[feature]) for feature in features]
        prediction = diabetes_model.predict([input_features])[0]
        result = "Diabetic" if prediction == 1 else "Non-Diabetic"
        return templates.TemplateResponse("result_diabetes.html", {"request": request, "result": result})
    
    return {"error": "Invalid disease type"}
