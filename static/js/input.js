const breastCancerFields = [
  "Radius Mean", "Texture Mean", "Perimeter Mean", "Area Mean", "Smoothness Mean",
  "Compactness Mean", "Concavity Mean", "Concave Points Mean", "Symmetry Mean", "Fractal Dimension Mean",
  "Radius SE", "Texture SE", "Perimeter SE", "Area SE", "Smoothness SE",
  "Compactness SE", "Concavity SE", "Concave Points SE", "Symmetry SE", "Fractal Dimension SE",
  "Radius Worst", "Texture Worst", "Perimeter Worst", "Area Worst", "Smoothness Worst",
  "Compactness Worst", "Concavity Worst", "Concave Points Worst", "Symmetry Worst", "Fractal Dimension Worst"
];

const diabetesFields = [
  "Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness", "Insulin",
  "BMI", "Diabetes Pedigree Function", "Age"
];

function updateFields() {
  const disease = document.getElementById("disease").value;
  const container = document.getElementById("feature-fields");
  const image = document.getElementById("disease-img");
  container.innerHTML = "";

  let fields = [];
  if (disease === "Breast Cancer") {
    fields = breastCancerFields;
    image.src = "/static/syringe.png";
  } else if (disease === "Diabetes") {
    fields = diabetesFields;
    image.src = "/static/sugar.png";
  }

  fields.forEach((label, i) => {
    const div = document.createElement("div");
    div.className = "input-group";
    div.innerHTML = `
      <label>${label}:</label>
      <input type="number" step="any" id="field_${i}" required>
    `;
    container.appendChild(div);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  updateFields();

  document.querySelector("form").addEventListener("submit", function (e) {
    const inputs = document.querySelectorAll("#feature-fields input");
    const values = Array.from(inputs).map(input => input.value.trim());
    document.getElementById("feature_values").value = values.join(",");
  });
});
