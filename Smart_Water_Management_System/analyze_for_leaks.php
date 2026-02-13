<?php
// Include database connection
require 'db_connect.php';

// Define the flow rate threshold for detecting potential leaks
$leak_threshold = 0.4; // Consider moving this to a config file or database setting

try {
    // Retrieve average flow rates for each sensor
    $query = "SELECT sensor_id, AVG(water_flow_rate) AS avg_flow 
              FROM water_usage_logs 
              GROUP BY sensor_id 
              HAVING avg_flow < ?";
    $stmt = $conn->prepare($query); // Changed $connection to $conn for consistency
    $stmt->bind_param("d", $leak_threshold);
    $stmt->execute();
    $result = $stmt->get_result();

    // Process sensors with abnormal flow rates
    while ($sensor = $result->fetch_assoc()) {
        $sensor_id = $sensor['sensor_id'];

        // Check if there's already an active alert for this sensor
        $alert_query = "SELECT * FROM leakage_alerts WHERE sensor_id = ? AND status = 'unresolved'";
        $alert_stmt = $conn->prepare($alert_query);
        $alert_stmt->bind_param("i", $sensor_id);
        $alert_stmt->execute();
        $alert_result = $alert_stmt->get_result();

        if ($alert_result->num_rows === 0) {
            // Log a new alert for the sensor
            $insert_alert = "INSERT INTO leakage_alerts (sensor_id) VALUES (?)";
            $insert_stmt = $conn->prepare($insert_alert);
            $insert_stmt->bind_param("i", $sensor_id);
            $insert_stmt->execute();
            $insert_stmt->close();
        }

        $alert_stmt->close();
    }

    $stmt->close();
    $conn->close();

    echo json_encode([
        "status" => "success",
        "message" => "Leak analysis completed."
    ]);
} catch (Exception $e) {
    echo json_encode([
        "status" => "error",
        "message" => "An error occurred: " . $e->getMessage()
    ]);
}
?>
