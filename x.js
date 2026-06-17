async function loadTrafficData() {
    try {
        const response = await fetch('/Modules/traffic_report.json');
        const data = await response.json();
        
        // Lấy bản ghi mới nhất
        const latest = data[data.length - 1];
        
        console.log(`Nhịp tim hệ thống: ${latest.status}`);
        
        // Logic cộng sinh: Nếu lỗi 404 hoặc 500, kích hoạt chế độ dự phòng
        if (latest.status !== 200) {
            console.warn("Phát hiện lỗi hạ tầng! Chuyển sang chế độ bảo mật...");
            // Thêm logic chuyển hướng hoặc thông báo tại đây
        }
    } catch (e) {
        console.error("Không thể kết nối với trạm quan trắc Modules/traffic_report.json");
    }
}
loadTrafficData();
