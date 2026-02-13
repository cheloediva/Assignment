<?php
require_once 'db_connect.php';

$alert_id = filter_input(INPUT_POST, 'alert_id', FILTER_VALIDATE_INT);
if (!$alert_id) {
    echo json_encode(['status' => 'error', 'message' => 'Invalid alert ID.']);
    exit();
}

$query = "UPDATE leakage_alerts SET status = 'resolved' WHERE alert_id = ?";
$stmt = $conn->prepare($query);
$stmt->bind_param('i', $alert_id);

if ($stmt->execute()) {
    echo json_encode(['status' => 'success', 'message' => 'Alert resolved successfully.']);
} else {
    echo json_encode(['status' => 'error', 'message' => 'Failed to resolve alert.']);
}

$stmt->close();
$conn->close();
?>
