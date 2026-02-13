// Load Dashboard Data
async function loadDashboard() {
    const response = await fetch('get_dashboard_data.php');
    const data = await response.json();

    document.getElementById('total-sensors').innerText = data.total_sensors;
    document.getElementById('active-alerts').innerText = data.active_alerts;
}

// Load Sensors
async function loadSensors() {
    const response = await fetch('get_sensors.php');
    const sensors = await response.json();

    const sensorTable = document.querySelector('#sensor-table tbody');
    sensorTable.innerHTML = '';

    sensors.forEach(sensor => {
        const row = `<tr>
            <td>${sensor.sensor_id}</td>
            <td>${sensor.location}</td>
            <td>${sensor.status}</td>
            <td>${sensor.type}</td>
        </tr>`;
        sensorTable.innerHTML += row;
    });
}

// Load Alerts
async function loadAlerts() {
    const response = await fetch('get_alerts.php');
    const alerts = await response.json();

    const alertTable = document.getElementById('alerts-table');
    alertTable.innerHTML = '';

    alerts.forEach(alert => {
        const row = `<tr>
            <td>${alert.alert_id}</td>
            <td>${alert.sensor_id}</td>
            <td>${alert.timestamp}</td>
            <td>${alert.status}</td>
        </tr>`;
        alertTable.innerHTML += row;
    });
}

// Load Water Logs
async function loadLogs() {
    const response = await fetch('get_water_logs.php?limit=50&offset=0'); // Specify pagination if necessary
    const logs = await response.json();

    const logsTable = document.getElementById('water-logs-table');
    logsTable.innerHTML = ''; // Clear previous content

    // Check if logs exist
    if (logs.length === 0) {
        logsTable.innerHTML = '<tr><td colspan="4">No logs available</td></tr>';
        return;
    }

    logs.forEach(log => {
        const row = `<tr>
            <td>${log.log_id}</td>
            <td>${log.sensor_id}</td>
            <td>${log.timestamp}</td>
            <td>${log.water_flow_rate}</td>
        </tr>`;
        logsTable.innerHTML += row;
    });
}

// Call the function to load logs
loadLogs();



// Initialize the interface
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
    loadSensors();
    loadAlerts();
    loadLogs();
});
document.getElementById('add-sensor-form').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Sensor added successfully!');
});

document.getElementById('create-user-form').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('User created successfully!');
});
