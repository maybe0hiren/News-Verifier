document.getElementById('check-btn').addEventListener('click', async () => {
  const inputValue = document.getElementById('news-input').value.trim();
  const outputDiv = document.getElementById('output');

  // Clear previous results
  outputDiv.innerHTML = "";

  if (inputValue === "") {
    outputDiv.textContent = "Please enter some news content or URL!";
    return;
  }

  try {
    const response = await fetch('http://localhost:5000/api/process', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: inputValue })
    });

    if (!response.ok) {
      outputDiv.textContent = "Error: Could not check news reliability.";
      return;
    }

    const result = await response.json();

    // Expecting result to be a list of segments (strings)
    if (Array.isArray(result)) {
      outputDiv.innerHTML = "<strong>Detected Context Segments:</strong><ul>"
        result.map(seg => `<li>${seg}</li>`).join('') +
        "</ul>";
    } else {
      outputDiv.textContent = "Unexpected result format from server.";
    }
  } catch (error) {
    outputDiv.textContent = "Error connecting to backend: " + error.message;
  }
});
