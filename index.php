<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Form</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #071E22;
            margin: 0;
            padding: 0;
            justify-content: center;
            align-items: center;
            display: flex;
            height: 100vh;
            color: #EE213E;
        }

        .container {
            background-color: #679289;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 30px;
            max-width: 400px;
            width: 100%;
            position: relative; /* Make container position relative */
            animation: slideUp 3s ease forwards; /* Apply animation */
            margin-right: 20px; /* Add space between container and logo */
            color: #EE213E;
        }

        .finalmsg {
            text-align: center;
            margin-top: 20px;
        }

        .logo {
            width: 30%; /* Set logo width to be smaller */
            height: auto; /* Maintain aspect ratio */
            opacity: 1.0;
            animation: slideUp 1s ease forwards;
        }

        .logo-container {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
        }

        @keyframes slideUp {
            0% {
                transform: translateY(50%);
            }
            100% {
                transform: translateY(0);
            }
        }

        h2 {
            text-align: center;
            color: #333;
        }

        form {
            margin-top: 20px;
        }

        input[type="file"],
        textarea,
        input[type="submit"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: none;
            border-radius: 5px;
            box-sizing: border-box;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: box-shadow 0.3s ease;
        }

        input[type="file"],
        textarea {
            resize: none;
            background-color: #1D7874;
            color: #F4C095;
        }

        input[type="file"]:hover,
        textarea:hover,
        input[type="submit"]:hover {
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        input[type="submit"] {
            background-color: #1D7874;
            color: #EE213E;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        input[type="submit"]:hover {
            background-color: #F4C095;
        }
        ::placeholder{
            color: #679289;
        }

        input::file-selector-button {
            font-weight: bold;
            color: #1D7874;
            padding: 0.5em;
            border: thin solid grey;
            border-radius: 3px;
        }
    </style>


</head>
<body>
    <div class="logo-container">
        <img src="assurant-logo.png" alt="Logo" class="logo">
        <div class="container">
            <h2>Upload an Image and Text</h2>
            <form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post" enctype="multipart/form-data">
                <input type="file" name="image" accept="image/*" required>
                <textarea name="text" rows="4" cols="50" placeholder="Enter your text here" required></textarea>
                <input type="submit" name="submit" value="Upload">
                <a href="report.php" class="report-btn">Go to Report Page</a>
            </form>
       
<div class = "finalmsg">

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        // Database connection
        $servername = "localhost";
        $username = "root";
        $password = "";
        $dbname = "hacklytics";

        $conn = new mysqli($servername, $username, $password, $dbname);
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        // Check if the directory exists, if not, create it
        if (!file_exists('uploads')) {
            mkdir('uploads', 0777, true);
        }

        // File upload
        $target_dir = "uploads/";
        $target_file = $target_dir . basename($_FILES["image"]["name"]);
        $uploadOk = 1;
        $imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

        // Check file size
        if ($_FILES["image"]["size"] > 500000) {
            echo "Sorry, your file is too large.";
            $uploadOk = 0;
        }

        // Allow certain file formats
        if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg"
        && $imageFileType != "gif" ) {
            echo "Sorry, only JPG, JPEG, PNG & GIF files are allowed.";
            $uploadOk = 0;
        }

        // Check if $uploadOk is set to 0 by an error
        if ($uploadOk == 0) {
            echo "Sorry, your file was not uploaded.";
        // if everything is ok, try to upload file
        } else {
            if (move_uploaded_file($_FILES["image"]["tmp_name"], $target_file)) {
                echo "The file ". basename( $_FILES["image"]["name"]). " has been uploaded.";

                // Insert into database
                $image_path = $target_file;
                $text_paragraph = $_POST['text'];
                $sql = "INSERT INTO uploads (image_path, text_paragraph) VALUES ('$image_path', '$text_paragraph')";
                if ($conn->query($sql) === TRUE) {
                    echo "New record created successfully";
                } else {
                    echo "Error: " . $sql . "<br>" . $conn->error;
                }
            } else {
                echo "Sorry, there was an error uploading your file.";
            }
        }

        $conn->close();
    }
    ?>
</div>
</div>
    </div>
</body>
</html>