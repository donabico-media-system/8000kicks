async function checkStatus() {
    try {
        const response = await fetch('Modules/traffic_report.json');
        const data = await response.json();
        const latest = data[data.length - 1];
        console.log("Status hiện tại:", latest.status);
    } catch (err) {
        console.error("Lỗi đọc file log:", err);
    }
}
checkStatus();
