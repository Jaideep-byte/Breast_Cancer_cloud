const diseaseSelect = document.getElementById("disease");
const featureInputs = document.getElementById("feature-inputs");

const breastCancerFeatures = [
    "Radius Mean", "Texture Mean", "Perimeter Mean", "Area Mean", "Smoothness Mean",
    "Compactness Mean", "Concavity Mean", "Concave Points Mean", "Symmetry Mean", "Fractal Dimension Mean",
    "Radius SE", "Texture SE", "Perimeter SE", "Area SE", "Smoothness SE",
    "Compactness SE", "Concavity SE", "Concave Points SE", "Symmetry SE", "Fractal Dimension SE",
    "Radius Worst", "Texture Worst", "Perimeter Worst", "Area Worst", "Smoothness Worst",
    "Compactness Worst", "Concavity Worst", "Concave Points Worst", "Symmetry Worst", "Fractal Dimension Worst"
];

const diabetesFeatures = [
    "Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness", "Insulin",
    "BMI", "Diabetes Pedigree Function", "Age"
];

function createInputs(features) {
    featureInputs.innerHTML = '';
    features.forEach((feature, index) => {
        const input = document.createElement("input");
        input.type = "number";
        input.name = `feature${index}`;
        input.placeholder = feature;
        input.required = true;
        featureInputs.appendChild(input);
    });
}

diseaseSelect.addEventListener("change", () => {
    if (diseaseSelect.value === "Breast Cancer") {
        createInputs(breastCancerFeatures);
    } else {
        createInputs(diabetesFeatures);
    }
});

window.addEventListener("DOMContentLoaded", () => {
    createInputs(breastCancerFeatures); // default
});
document.addEventListener("DOMContentLoaded", () => {
    console.log("Input page loaded.");
});