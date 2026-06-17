async function activateSymbiosis() {
    try {
        const response = await fetch('/traffic_report.json');
        const data = await response.json();
        const latest = data[data.length - 1]; // Lấy lần kiểm tra mới nhất

        const statusElement = document.getElementById('status-indicator');
        if (latest.status === 200) {
            statusElement.innerText = "Hệ thống đang hoạt động ổn định";
            statusElement.style.color = "green";
        } else {
            statusElement.innerText = "Hệ thống đang bảo trì";
            statusElement.style.color = "red";
        }
    } catch (e) {
        console.log("Cộng sinh tạm gián đoạn...");
    }
}
activateSymbiosis();
