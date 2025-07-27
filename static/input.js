const diseaseSelect = document.getElementById("disease");
const featureContainer = document.getElementById("feature-container");
const image = document.getElementById("disease-image");

const cancerFeatures = [
  "Radius Mean", "Texture Mean", "Perimeter Mean", "Area Mean", "Smoothness Mean",
  "Compactness Mean", "Concavity Mean", "Concave Points Mean", "Symmetry Mean", "Fractal Dimension Mean",
  "Radius SE", "Texture SE", "Perimeter SE", "Area SE", "Smoothness SE",
  "Compactness SE", "Concavity SE", "Concave Points SE", "Symmetry SE", "Fractal Dimension SE",
  "Radius Worst", "Texture Worst", "Perimeter Worst", "Area Worst", "Smoothness Worst",
  "Compactness Worst", "Concavity Worst", "Concave Points Worst", "Symmetry Worst", "Fractal Dimension Worst"
];

const diabetesFeatures = [
  "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
  "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
];

diseaseSelect.addEventListener("change", () => {
  const disease = diseaseSelect.value;
  featureContainer.innerHTML = ""; // Clear previous inputs

  let features = [];
  if (disease === "cancer") {
    features = cancerFeatures;
    image.src = "/static/syringe.png";
  } else if (disease === "diabetes") {
    features = diabetesFeatures;
    image.src = "/static/sugar.png";
  } else {
    image.src = "/static/heart_hands.png";
  }

  // Generate input fields
  features.forEach((feature, index) => {
    const wrapper = document.createElement("div");

    const label = document.createElement("label");
    label.htmlFor = disease === "cancer" ? `feature${index}` : feature;
    label.textContent = feature;

    const input = document.createElement("input");
    input.type = "number";
    input.step = "any";
    input.name = disease === "cancer" ? `feature${index}` : feature;
    input.required = true;

    wrapper.appendChild(label);
    wrapper.appendChild(input);
    featureContainer.appendChild(wrapper);
  });
});
