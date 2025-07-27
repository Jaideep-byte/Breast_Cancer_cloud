document.addEventListener("DOMContentLoaded", () => {
  const diseaseSelect = document.getElementById("disease");
  const featureContainer = document.getElementById("feature-container");
  const diseaseImage = document.getElementById("disease-image");
  const hiddenDisease = document.getElementById("hidden-disease");

  diseaseSelect.addEventListener("change", () => {
    const disease = diseaseSelect.value;
    hiddenDisease.value = disease;
    featureContainer.innerHTML = "";

    if (disease === "cancer") {
      for (let i = 1; i <= 30; i++) {
        const div = document.createElement("div");
        div.className = "input-field";
        div.innerHTML = `
          <label for="feature${i}">Feature ${i}</label>
          <input type="number" name="feature${i}" step="any" required />
        `;
        featureContainer.appendChild(div);
      }
      diseaseImage.src = "/static/syringe.png";
    } else if (disease === "diabetes") {
      const labels = [
        "Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness",
        "Insulin", "BMI", "Diabetes Pedigree Function", "Age"
      ];
      labels.forEach((label, i) => {
        const div = document.createElement("div");
        div.className = "input-field";
        div.innerHTML = `
          <label for="feature${i + 1}">${label}</label>
          <input type="number" name="feature${i + 1}" step="any" required />
        `;
        featureContainer.appendChild(div);
      });
      diseaseImage.src = "/static/sugar.png";
    } else {
      diseaseImage.src = "/static/heart_hands.png";
    }
  });
});
