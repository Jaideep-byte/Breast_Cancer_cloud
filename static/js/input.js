function renderInputs(disease) {
  const container = document.getElementById("form-fields");
  container.innerHTML = "";
  let fields = [];

  if (disease === "cancer") {
    fields = [
      "Radius Mean", "Texture Mean", "Perimeter Mean", "Area Mean", "Smoothness Mean",
      "Compactness Mean", "Concavity Mean", "Concave Points Mean", "Symmetry Mean", "Fractal Dimension Mean",
      "Radius SE", "Texture SE", "Perimeter SE", "Area SE", "Smoothness SE",
      "Compactness SE", "Concavity SE", "Concave Points SE", "Symmetry SE", "Fractal Dimension SE",
      "Radius Worst", "Texture Worst", "Perimeter Worst", "Area Worst", "Smoothness Worst",
      "Compactness Worst", "Concavity Worst", "Concave Points Worst", "Symmetry Worst", "Fractal Dimension Worst"
    ];
  } else if (disease === "diabetes") {
    fields = [
      "Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness",
      "Insulin", "BMI", "Diabetes Pedigree Function", "Age"
    ];
  }

  fields.forEach((field, index) => {
    const label = document.createElement("label");
    label.textContent = field;
    label.htmlFor = `f${index}`;

    const input = document.createElement("input");
    input.type = "number";
    input.step = "any";
    input.name = `f${index}`;
    input.required = true;

    container.appendChild(label);
    container.appendChild(input);
  });
}
