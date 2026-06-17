async function activateSymbiosis() {
    try {
        const response = await fetch('/traffic_report.json');
        const data = await response.json();
        const latest = data[data.length - 1];

        // Nếu trạng thái hệ thống không phải 200, tự động chuyển hướng khách hàng
        if (latest.status !== 200) {
            console.log("Hệ thống gián đoạn, đang chuyển hướng...");
            window.location.href = "https://your-backup-domain.com"; // Link dự phòng của bạn
        } else {
            console.log("Hệ thống hoạt động bình thường.");
        }
    } catch (e) {
        console.log("Đang kiểm tra kết nối...");
    }
}
activateSymbiosis();
