const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

// Set up multer for file uploads
const storage = multer.diskStorage({
    destination: './uploads/',
    filename: function(req, file, cb) {
        cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
    }
});

const upload = multer({
    storage: storage
}).single('imageInput');

// Set up static directory for serving HTML, CSS, and client-side JS
app.use(express.static('public'));

// Handle POST request to /upload
app.post('/upload', (req, res) => {
    upload(req, res, (err) => {
        if (err) {
            console.error('Error uploading file:', err);
            res.status(500).json({ message: 'Error uploading file.' });
        } else {
            console.log('File uploaded successfully:', req.file);

            if (req.file && req.file.path) {
                // Construct the data object with image path and text input
                const data = {
                    imagePath: req.file.path.replace(/\\/g, '/'), // Replace backslashes with forward slashes
                    textInput: req.body.textInput
                };

                console.log('Data to be saved:', data);

                // Convert the data object to JSON format
                const jsonData = JSON.stringify(data, null, 2);

                // Define the file path where the data will be saved
                const filePath = './data.json';

                // Write the JSON data to the file
                fs.writeFile(filePath, jsonData, 'utf8', (err) => {
                    if (err) {
                        console.error('Error saving data:', err);
                        res.status(500).json({ message: 'Error saving data.' });
                    } else {
                        console.log('Data saved successfully.');
                        // Send response to the client
                        res.json({ message: 'Data saved successfully.' });
                    }
                });
            } else {
                res.status(400).json({ message: 'Image path not found in the request.' });
            }
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
