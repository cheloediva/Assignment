<?php
require_once 'db_connect.php';

$query = "SELECT sensor_id, location, status, type FROM sensors";
$result = $conn->query($query);

$sensors = [];
if ($result) {
    while ($row = $result->fetch_assoc()) {
        $sensors[] = $row;
    }
} else {
    die("Error retrieving sensors: " . $conn->error); // Handle query error
}

// Return JSON response
header('Content-Type: application/json');
echo json_encode($sensors);
?>
