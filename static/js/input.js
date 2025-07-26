const cancerFeatures = [
    "radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean",
    "compactness_mean", "concavity_mean", "concave points_mean", "symmetry_mean", "fractal_dimension_mean",
    "radius_se", "texture_se", "perimeter_se", "area_se", "smoothness_se",
    "compactness_se", "concavity_se", "concave points_se", "symmetry_se", "fractal_dimension_se",
    "radius_worst", "texture_worst", "perimeter_worst", "area_worst", "smoothness_worst",
    "compactness_worst", "concavity_worst", "concave points_worst", "symmetry_worst", "fractal_dimension_worst"
];

const diabetesFeatures = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin",
    "BMI", "DiabetesPedigreeFunction", "Age"
];

const form = document.getElementById("prediction-form");
const inputContainer = document.getElementById("feature-inputs");
const diseaseSelector = document.getElementById("disease");
const image = document.getElementById("disease-image");

function renderFields(features) {
    inputContainer.innerHTML = "";
    features.forEach((feature, index) => {
        const fieldDiv = document.createElement("div");

        const label = document.createElement("label");
        label.htmlFor = `feature${index}`;
        label.innerText = feature.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase());

        const input = document.createElement("input");
        input.type = "number";
        input.step = "any";
        input.name = `feature${index}`;
        input.placeholder = feature;

        fieldDiv.appendChild(label);
        fieldDiv.appendChild(input);
        inputContainer.appendChild(fieldDiv);
    });
}

function updateFormAction(disease) {
    if (disease === "diabetes") {
        form.action = "/predict/diabetes";
        renderFields(diabetesFeatures);
        image.src = "/static/images/sugar.png";
        image.alt = "Sugar Icon";
    } else {
        form.action = "/predict/cancer";
        renderFields(cancerFeatures);
        image.src = "/static/images/syringe.png";
        image.alt = "Syringe Icon";
    }
}

diseaseSelector.addEventListener("change", () => {
    updateFormAction(diseaseSelector.value);
});

// Initial render
updateFormAction(diseaseSelector.value);
