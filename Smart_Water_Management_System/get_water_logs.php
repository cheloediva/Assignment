<?php
require_once 'db_connect.php';

// Add pagination
$limit = isset($_GET['limit']) ? intval($_GET['limit']) : 50; // Default 50 logs
$offset = isset($_GET['offset']) ? intval($_GET['offset']) : 0;

$query = "SELECT log_id, sensor_id, timestamp, water_flow_rate 
          FROM water_usage_logs 
          LIMIT ? OFFSET ?";
$stmt = $conn->prepare($query);
$stmt->bind_param("ii", $limit, $offset);
$stmt->execute();
$result = $stmt->get_result();

$logs = [];
if ($result) {
    while ($row = $result->fetch_assoc()) {
        // Ensure timestamp is formatted correctly
        $row['timestamp'] = date('Y-m-d H:i:s', strtotime($row['timestamp']));
        $logs[] = $row;
    }
}

// Return JSON response
header('Content-Type: application/json');
echo json_encode($logs);
?>
