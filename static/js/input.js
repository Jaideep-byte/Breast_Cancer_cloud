function renderFields() {
    const disease = document.getElementById("disease").value;
    const formFields = document.getElementById("formFields");
    formFields.innerHTML = "";

    let count = disease === "cancer" ? 30 : 8;
    for (let i = 0; i < count; i++) {
        let input = document.createElement("input");
        input.type = "number";
        input.step = "any";
        input.name = "feature";
        input.placeholder = `Feature ${i + 1}`;
        input.required = true;
        formFields.appendChild(input);
        formFields.appendChild(document.createElement("br"));
    }
}

async function handleSubmit(event) {
    event.preventDefault();
    const disease = document.getElementById("disease").value;
    const form = document.getElementById("inputForm");
    const features = Array.from(form.querySelectorAll("input[name='feature']")).map(input => parseFloat(input.value));

    let endpoint = disease === "cancer" ? "/predict_cancer" : "/predict_diabetes";
    const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ features })
    });

    const result = await response.json();
    const resultPage = disease === "cancer" ? "result_cancer" : "result_diabetes";
    const queryParams = new URLSearchParams(result).toString();
    window.location.href = `/${resultPage}?${queryParams}`;
}
