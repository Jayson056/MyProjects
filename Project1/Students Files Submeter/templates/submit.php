<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST["name"];
    $email = $_POST["email"];

    $resume = $_FILES["resume"];
    $resumeFileName = $resume["name"];
    $resumeTmpName = $resume["tmp_name"];
    $to = "jaysonc864@gmail.com";
    $subject = "New Student Information";
    $message = "Name: $name\nEmail: $email";
    $headers = "From: $email\r\nReply-To: $email\r\n";
    mail($to, $subject, $message, $headers);
    $uploadDir = "uploads/";

    if (!file_exists($uploadDir)) {
        mkdir($uploadDir, 0777, true);
    }
    $uploadPath = $uploadDir . $resumeFileName;
    move_uploaded_file($resumeTmpName, $uploadPath);

    header("Location: /thank-you.html");
    exit();
}
?>
