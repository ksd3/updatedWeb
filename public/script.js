document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData();
    const imageInput = document.getElementById('imageInput').files[0];
    const textInput = document.getElementById('textInput').value;

    formData.append('imageInput', imageInput);
    formData.append('textInput', textInput);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        console.log(result);
        // document.getElementById('output').innerHTML = `<p>Image path: ${result.imagePath}</p>`;
    } catch (error) {
        console.error('Error:', error);
    }
});
