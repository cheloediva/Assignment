<?php
// password_hash.php
// Example of hashing a password securely
$password = 'admin123'; // Replace with the actual password
$hashedPassword = password_hash($password, PASSWORD_DEFAULT); // Securely hash the password

// Print hashed password (copy this output and use it in your database for comparison)
echo $hashedPassword;
?>
