<?php
require_once 'db_connect.php';

$response = [
    'total_sensors' => 100,
    'active_alerts' => 10,
];

$querySensors = "SELECT COUNT(*) AS total FROM sensors";
$queryAlerts = "SELECT COUNT(*) AS total FROM leakage_alerts WHERE status = 'unresolved'";

$resultSensors = $conn->query($querySensors);
$resultAlerts = $conn->query($queryAlerts);

if ($resultSensors && $row = $resultSensors->fetch_assoc()) {
    $response['total_sensors'] = $row['total'];
}

if ($resultAlerts && $row = $resultAlerts->fetch_assoc()) {
    $response['active_alerts'] = $row['total'];
}

header('Content-Type: application/json');
echo json_encode($response);
?>

