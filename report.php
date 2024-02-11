<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            border: 1px solid #dddddd;
            padding: 8px;
            text-align: left;
        }

        th {
            background-color: #f2f2f2;
        }

        tr:nth-child(even) {
            background-color: #f2f2f2;
        }

        tr:hover {
            background-color: #dddddd;
        }
    </style>
</head>
<body>
    <?php
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "hacklytics";
    
    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);
    
    // Check connection
    if ($conn->connect_error) {
      die("Connection failed: " . $conn->connect_error);
    }
    
    $sql = "SELECT image_path, text_output FROM uploads";
    $result = $conn->query($sql);

    if($result->num_rows > 0){
        echo "<table><tr><th>Image</th><th>Text Output</th></tr>";

        while($row = $result->fetch_assoc()){
            echo "<tr><td>" . "<img src = \" ". $row["image_path"] . "\"></td><td>" . $row["text_output"] . "</td></tr>";
        }
        echo "</table>";
    }else{
            echo "0 results";
        }
    

    $conn->close();

    ?>
</body>
</html>