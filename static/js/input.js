document.addEventListener("DOMContentLoaded", function () {
  const diseaseSelect = document.getElementById("disease");
  const featureContainer = document.getElementById("feature-container");
  const image = document.getElementById("disease-image");

  const diabetesFields = [
    "Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness",
    "Insulin", "BMI", "Diabetes Pedigree Function", "Age"
  ];

  const cancerFields = [
    "Radius Mean", "Texture Mean", "Perimeter Mean", "Area Mean", "Smoothness Mean",
    "Compactness Mean", "Concavity Mean", "Concave Points Mean", "Symmetry Mean", "Fractal Dimension Mean",
    "Radius SE", "Texture SE", "Perimeter SE", "Area SE", "Smoothness SE",
    "Compactness SE", "Concavity SE", "Concave Points SE", "Symmetry SE", "Fractal Dimension SE",
    "Radius Worst", "Texture Worst", "Perimeter Worst", "Area Worst", "Smoothness Worst",
    "Compactness Worst", "Concavity Worst", "Concave Points Worst", "Symmetry Worst", "Fractal Dimension Worst"
  ];

  function renderFields(fields, namePrefix) {
    featureContainer.innerHTML = "";
    fields.forEach((field, i) => {
      const label = document.createElement("label");
      label.textContent = field;
      label.setAttribute("for", `${namePrefix}${i}`);
      label.className = "input-label";

      const input = document.createElement("input");
      input.type = "number";
      input.step = "any";
      input.name = field.toLowerCase().replace(/\s+/g, "_");
      input.required = true;
      input.className = "input-field";

      const div = document.createElement("div");
      div.className = "input-box";
      div.appendChild(label);
      div.appendChild(input);

      featureContainer.appendChild(div);
    });
  }

  diseaseSelect.addEventListener("change", function () {
    const selectedDisease = diseaseSelect.value;
    if (selectedDisease === "diabetes") {
      renderFields(diabetesFields, "diabetes");
      image.src = "/static/sugar.png";
    } else if (selectedDisease === "cancer") {
      renderFields(cancerFields, "cancer");
      image.src = "/static/syringe.png";
    } else {
      featureContainer.innerHTML = "";
      image.src = "/static/heart_hands.png";
    }
  });

  // Initial trigger
  diseaseSelect.dispatchEvent(new Event("change"));
});
