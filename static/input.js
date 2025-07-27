const diseaseSelect = document.getElementById("disease");
const featureContainer = document.getElementById("feature-container");
const diseaseImage = document.getElementById("disease-image");
const hiddenDiseaseInput = document.getElementById("hidden-disease");

const cancerFeatures = [
  "Radius Mean", "Texture Mean", "Perimeter Mean", "Area Mean", "Smoothness Mean",
  "Compactness Mean", "Concavity Mean", "Concave Points Mean", "Symmetry Mean", "Fractal Dimension Mean",
  "Radius SE", "Texture SE", "Perimeter SE", "Area SE", "Smoothness SE",
  "Compactness SE", "Concavity SE", "Concave Points SE", "Symmetry SE", "Fractal Dimension SE",
  "Radius Worst", "Texture Worst", "Perimeter Worst", "Area Worst", "Smoothness Worst",
  "Compactness Worst", "Concavity Worst", "Concave Points Worst", "Symmetry Worst", "Fractal Dimension Worst"
];

const diabetesFeatures = [
  "Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness",
  "Insulin", "BMI", "Diabetes Pedigree Function", "Age"
];

diseaseSelect.addEventListener("change", () => {
  const selectedDisease = diseaseSelect.value;
  hiddenDiseaseInput.value = selectedDisease;

  // Change image
  if (selectedDisease === "cancer") {
    diseaseImage.src = "/static/syringe.png";
    generateInputs(cancerFeatures);
  } else if (selectedDisease === "diabetes") {
    diseaseImage.src = "/static/sugar.png";
    generateInputs(diabetesFeatures);
  } else {
    featureContainer.innerHTML = "";
    diseaseImage.src = "/static/heart_hands.png";
  }
});

function generateInputs(features) {
  featureContainer.innerHTML = "";
  features.forEach((feature, index) => {
    const div = document.createElement("div");
    div.className = "input-group";

    const label = document.createElement("label");
    label.innerText = feature;
    label.setAttribute("for", `feature_${index}`);

    const input = document.createElement("input");
    input.type = "number";
    input.step = "any";
    input.name = `feature_${index}`;
    input.id = `feature_${index}`;
    input.required = true;

    div.appendChild(label);
    div.appendChild(input);
    featureContainer.appendChild(div);
  });
}
// Initialize with default disease