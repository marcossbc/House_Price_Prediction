document.getElementById("predictForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const payload = {
        Size_m2: parseFloat(document.getElementById("Size_m2").value),
        Bedrooms: parseInt(document.getElementById("Bedrooms").value),
        Bathrooms: parseInt(document.getElementById("Bathrooms").value),
        YearBuilt: parseInt(document.getElementById("YearBuilt").value),
        Location: document.getElementById("Location").value
    };

    const model = document.getElementById("modelChoice").value;
    const resultDiv = document.getElementById("result");
    const predictButton = e.target.querySelector("button[type='submit']");
    
    // Nadiifi class-ka oo u deji Loading State
    predictButton.innerText = "Predicting...";
    predictButton.disabled = true;
    resultDiv.className = "result-loading";
    resultDiv.innerHTML = `<img width="30" height="30" src="https://img.icons8.com/dotty/80/spinner-frame-3.png" alt="loading"/> **Xisaabinaynaa qiimaha...**`;

    try {
        const res = await fetch(`http://localhost:8000/predict?model=${model}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        
        // Error Handling
        if (data.error) {
            resultDiv.className = "result-error";
            resultDiv.innerHTML = "❌ Qalad: " + data.error;
        } else {
            // Success State
            resultDiv.className = "result-success";
            
            // Habee qiimaha si ay u muuqato sida $1,250.00
            const predictedPrice = parseFloat(data.prediction).toLocaleString('en-US', { 
                minimumFractionDigits: 0, 
                maximumFractionDigits: 2 
            });
            
            resultDiv.innerHTML = `
                <img width="40" height="40" 
                    src="https://img.icons8.com/3d-fluency/94/ok.png" 
                    alt="ok" style="vertical-align: middle; margin-right: 10px;">
                <p>Saadaasha Qiimaha Kirada (${data.model}): <br>
                <span style="font-size: 1.8em; color: #1e8449;"><b>$${predictedPrice}</b></span></p>
            `;
        }
    } catch (err) {
        // Server Connection Error
        resultDiv.className = "result-error";
        resultDiv.innerHTML = "⚠️ Qalad: Ma aannu xirmi karin Server-ka. Hubi in **Flask API**-gaagu uu shaqeynayo.";
    } finally {
        predictButton.innerText = "Predict Rent Price";
        predictButton.disabled = false;
    }
});