const breastCancerFeatures = [
    "Radius Mean", "Texture Mean", "Perimeter Mean", "Area Mean", "Smoothness Mean",
    "Compactness Mean", "Concavity Mean", "Concave Points Mean", "Symmetry Mean", "Fractal Dimension Mean",
    "Radius SE", "Texture SE", "Perimeter SE", "Area SE", "Smoothness SE",
    "Compactness SE", "Concavity SE", "Concave Points SE", "Symmetry SE", "Fractal Dimension SE",
    "Radius Worst", "Texture Worst", "Perimeter Worst", "Area Worst", "Smoothness Worst",
    "Compactness Worst", "Concavity Worst", "Concave Points Worst", "Symmetry Worst", "Fractal Dimension Worst"
];

const diabetesFeatures = [
    "Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness",
    "Insulin", "BMI", "Diabetes Pedigree", "Age"
];

function toggleDisease() {
    const disease = document.getElementById("disease").value;
    const fieldsContainer = document.getElementById("form-fields");
    const image = document.getElementById("disease-img");

    fieldsContainer.innerHTML = "";

    const features = disease === "Breast Cancer" ? breastCancerFeatures : diabetesFeatures;
    image.src = disease === "Breast Cancer" ? "/static/syringe.png" : "/static/sugar.png";

    features.forEach((name, i) => {
        const label = document.createElement("label");
        label.textContent = `${name}:`;
        label.setAttribute("for", `feature_${i}`);

        const input = document.createElement("input");
        input.type = "number";
        input.step = "any";
        input.name = `feature_${i}`;
        input.id = `feature_${i}`;
        input.required = true;

        fieldsContainer.appendChild(label);
        fieldsContainer.appendChild(input);
    });
}

document.addEventListener("DOMContentLoaded", toggleDisease);
