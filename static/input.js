const featureContainer = document.getElementById("feature-container");
const diseaseSelect = document.getElementById("disease");
const image = document.getElementById("disease-image");
const hiddenDisease = document.getElementById("hidden-disease");

const cancerFeatures = [
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

diseaseSelect.addEventListener("change", () => {
  const disease = diseaseSelect.value;
  hiddenDisease.value = disease;
  featureContainer.innerHTML = "";

  let features = [];
  if (disease === "cancer") {
    image.src = "/static/syringe.png";
    features = cancerFeatures;
  } else if (disease === "diabetes") {
    image.src = "/static/sugar.png";
    features = diabetesFeatures;
  } else {
    image.src = "/static/heart_hands.png";
  }

  features.forEach((feature, index) => {
    const div = document.createElement("div");
    div.className = "input-group";
    div.innerHTML = `
      <label for="feature_${index}">${feature}</label>
      <input type="number" step="any" name="feature_${index}" required />
    `;
    featureContainer.appendChild(div);
  });
});
// Trigger change event on page load to set initial state