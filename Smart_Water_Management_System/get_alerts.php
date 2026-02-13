<?php
require_once 'db_connect.php';

// Fetch active alerts
$query = "SELECT * FROM leakage_alerts WHERE status = 'unresolved'";
$result = $conn->query($query);

$alerts = [];
if ($result) {
    while ($row = $result->fetch_assoc()) {
        $alerts[] = $row;
    }
    
      
}

// Return JSON response
header('Content-Type: application/json');
echo json_encode($alerts);
?>
