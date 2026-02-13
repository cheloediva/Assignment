<?php
// Include database connection
require_once 'db_connect.php';

// Check for POST method
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['status' => 'error', 'message' => 'Invalid request method.']);
    exit;
}

// Get input data
$location = trim($_POST['location'] ?? '');
$type = trim($_POST['type'] ?? '');
$status = 'active'; // Default status

// Validate input
if (empty($location) || empty($type)) {
    echo json_encode(['status' => 'error', 'message' => 'Location and type are required.']);
    exit;
}

// Ensure the type is not NULL (if required)
if (is_null($type)) {
    echo json_encode(['status' => 'error', 'message' => 'Type cannot be null.']);
    exit;
}

try {
    // Insert new sensor into the database
    $query = "INSERT INTO sensors (location, type, status) VALUES (?, ?, ?)";
    $stmt = $conn->prepare($query);
    $stmt->bind_param('sss', $location, $type, $status); // Binding parameters with an explicit status value

    if ($stmt->execute()) {
        echo json_encode(['status' => 'success', 'message' => 'Sensor added successfully.']);
    } else {
        echo json_encode(['status' => 'error', 'message' => 'Failed to add sensor.']);
    }
} catch (Exception $e) {
    echo json_encode(['status' => 'error', 'message' => 'Database error: ' . $e->getMessage()]);
}
?>  