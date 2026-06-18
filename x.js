async function checkStatus() {
    try {
        // Gọi file log từ đúng phân mục hệ thống
        const response = await fetch('Modules/traffic_report.json');
        
        if (!response.ok) {
            throw new Error(`Mạng lỗi phản hồi không thành công: ${response.status}`);
        }

        const data = await response.json();
        
        // KIỂM TRA AN TOÀN: Đảm bảo mảng dữ liệu tồn tại và có phần tử để tránh sập luồng
        if (Array.isArray(data) && data.length > 0) {
            const latest = data[data.length - 1];
            
            // Sử dụng toán tử ?. để phòng ngừa biến cố mất cấu trúc trường dữ liệu status
            console.log("Status hiện tại:", latest?.status ?? "Không xác định");
        } else {
            console.log("Hệ thống cảnh báo: Cơ sở dữ liệu telemetry hiện đang rỗng.");
        }
    } catch (err) {
        console.error("Lỗi đọc file log:", err.message);
    }
}

// Khởi chạy tiến trình kiểm thử trạng thái
checkStatus();
