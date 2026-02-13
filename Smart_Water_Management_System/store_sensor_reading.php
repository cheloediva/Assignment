<?php
// Include database connection
require_once 'db_connect.php';

// Retrieve sensor data from POST request
$sensor_id = $_POST['sensor_id'] ?? null;
$reading = $_POST['reading'] ?? null; // e.g., flow rate or other metrics
$timestamp = date('Y-m-d H:i:s'); // Current timestamp

// Validate input
if (!$sensor_id || !$reading) {
    echo json_encode([
        'status' => 'error',
        'message' => 'Sensor ID and reading are required.',
    ]);
    exit();
}

// Insert the sensor reading into the database
$query = "INSERT INTO water_usage_logs (sensor_id, flow_rate, timestamp) VALUES (?, ?, ?)";
$stmt = $conn->prepare($query);
$stmt->bind_param('ids', $sensor_id, $reading, $timestamp);

if ($stmt->execute()) {
    echo json_encode([
        'status' => 'success',
        'message' => 'Sensor reading stored successfully.',
    ]);
} else {
    echo json_encode([
        'status' => 'error',
        'message' => 'Failed to store sensor reading.',
    ]);
}

// Close statement and connection
$stmt->close();
$conn->close();
?>
