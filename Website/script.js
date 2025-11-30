document.getElementById("uploadForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const imageFile = document.getElementById("imageInput").files[0];
    const caption = document.getElementById("captionInput").value;

    let formData = new FormData();
    formData.append("image", imageFile);
    formData.append("caption", caption);

    const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
    });

    const result = await response.json();
    document.getElementById("status").innerText = result.message;
});
