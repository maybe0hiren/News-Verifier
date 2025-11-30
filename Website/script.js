document.addEventListener("DOMContentLoaded", () => {
    const imageInput = document.getElementById("imageInput");
    const preview = document.getElementById("preview");
    const captionInput = document.getElementById("captionInput");
    const uploadBtn = document.getElementById("uploadBtn");
    const statusEl = document.getElementById("status");

    imageInput.addEventListener("change", () => {
        const file = imageInput.files[0];
        if (file) {
            preview.style.display = "block";
            preview.src = URL.createObjectURL(file);
        } else {
            preview.style.display = "none";
        }
    });

    uploadBtn.addEventListener("click", async () => {
        const imageFile = imageInput.files[0];
        const caption = captionInput.value.trim();

        if (!imageFile || !caption) {
            statusEl.innerText = "Please select an image and enter a caption.";
            return;
        }

        const formData = new FormData();
        formData.append("image", imageFile);
        formData.append("caption", caption);

        statusEl.innerText = "Processing...";

        try {
            const response = await fetch("http://127.0.0.1:5000/upload", {
                method: "POST",
                body: formData
            });

            const body = document.body;

            // If server error →
            if (!response.ok) {
                const errorBox = document.createElement("div");
                errorBox.classList.add("result-container");
                errorBox.innerHTML = `
                    <h2>TrueTrace Result</h2>
                    <p class="result-text">Server error. Try again.</p>
                `;

                document.querySelector(".container").remove();  
                body.appendChild(errorBox);
                return;
            }

            const result = await response.json();

            // Create NEW wider container
            const resultContainer = document.createElement("div");
            resultContainer.classList.add("result-container");

            resultContainer.innerHTML = `
                <h2>TrueTrace Result</h2>
                <p class="result-text">
                    ${result.result || "No result found"}
                </p>
            `;

            // Remove old container
            document.querySelector(".container").remove();

            // Add new wider container to body
            body.appendChild(resultContainer);

        } catch (err) {
            statusEl.innerText = "An error occurred: " + err.message;
        }
    });
});
