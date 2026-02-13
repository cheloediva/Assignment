<?php
session_start();
if (!isset($_SESSION['admin_id'])) {
    header("Location: admin_login.php");
    exit();
}

require_once 'db_connect.php';
?>
<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Admin Dashboard</h1>
    <p><a href="logout.php">Logout</a></p>
    <div class="dashboard-cards">
        <div class="card">
            <h3>Total Sensors</h3>
            <p id="total-sensors">Loading...</p>
        </div>
        <div class="card">
            <h3>Active Alerts</h3>
            <p id="active-alerts">Loading...</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>
