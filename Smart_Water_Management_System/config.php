<?php
// Database connection configuration
$host = "localhost";       // Replace with your server host
$username = "your_username"; // Replace with your database username
$password = "your_password"; // Replace with your database password
$database = "your_database"; // Replace with your database name

$conn = mysqli_connect($host, $username, $password, $database);

// Check for connection errors
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}
?>
