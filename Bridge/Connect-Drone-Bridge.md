# 🛸 DONABICO GLOBAL MEDIA SYSTEM - ADTECH INFRASTRUCTURE
## 🤖 MODULE: CONNECT DRONE BRIDGE (TÀI LIỆU VẬN HÀNH VỆ TINH)
---
### 📌 1. TỔNG QUAN CHIẾN THUẬT
Tài liệu này đặc tả cấu trúc kỹ thuật và nguyên lý phản hồi dữ liệu của tệp kết nối vệ tinh (`Modules/Connect-Drone-Bridge.py`) đặt tại **Kho 8000kicks** và các kho thương hiệu phân tán. 
Mã nguồn đóng vai trò làm cổng truyền tải thụ động tại thực địa. Khi nhận được xung lệnh đánh thức từ Tổng trạm Kho 4, mô-đun này sẽ tự động thu thập trạng thái các tệp nghiệp vụ tại chỗ, đóng gói dữ liệu và thiết lập đường truyền ngược lại trung tâm điều phối mà không lưu lại bất kỳ dấu vết bảo mật dài hạn nào tại vệ tinh.
---
### 🧬 2. TIẾN TRÌNH ĐỊNH TUYẾN PHẢN HỒI (RETURNING TOPOLOGY PROSE)
Tiến trình phản hồi mạng lưới được khởi động ngay khi tệp cấu hình tiếp nhận lệnh của vệ tinh được kích nổ thành công. Tại thực địa, tệp cầu nối sẽ lập tức nạp mã định danh ngắn hạn được Tổng trạm Kho 4 & Kho 2 chuyển giao qua biến môi trường bảo mật để làm chìa khóa mở cổng API. Ngay sau khi vượt qua bước kiểm tra khóa quyền hạn, hệ thống thực hiện quét sâu cấu trúc thư mục nội bộ nhằm bóc tách toàn bộ danh sách các mô-đun phụ trợ đang ở trạng thái hoạt động trực chiến.
Khi dữ liệu thực địa đã được thu thập đầy đủ, bộ mã hóa tiến hành đóng gói gói tin Payload theo đúng tiêu chuẩn cấu trúc ma trận rồi kích hoạt giao thức mạng truyền dữ liệu diện rộng. Luồng thông tin được bắn thẳng về endpoint đích của Tổng trạm Kho 4 dưới dạng sự kiện truyền thông. Nếu gặp sự cố nghẽn mạng do hệ thống GitHub Actions quá tải, mô-đun cầu nối tự động áp dụng thuật toán trì hoãn và tái phát xung tối đa ba lần liên tiếp để đảm bảo mạch máu thông tin AdTech được kết nối liền mạch, thông suốt về lõi trung tâm.
---
### ⚙️ 3. THÔNG SỐ KỸ THUẬT & BIẾN MÔI TRƯỜNG
Mô-đun vận hành hoàn toàn dựa trên cơ chế cấp phát quyền động ngắn hạn nhằm triệt tiêu rủi ro rò rỉ mã khóa:
* **Biến `BRIDGE_TOKEN`**: Mã định danh động được ký gửi trực tiếp từ xung lực điều phối của Kho 4. Trường hợp chạy kiểm thử độc lập tại chỗ, hệ thống sẽ tự động hạ cấp xuống sử dụng mã token nội bộ của kho vệ tinh.
#### 📊 Cấu trúc Gói tin Phản hồi (Payload Specification):
Gói tin phát đi sử dụng sự kiện định danh nhằm kích hoạt ngược lại chuỗi hành động xử lý tại Tổng trạm:
* **Event Type:** "DRONE_MESH_CONNECT" => Ánh Xạ Trực Tiếp Đến "ACTION WORKFLOW" Tại kho 4
* **Cấu trúc dữ liệu gửi về Kho 4:**
  * `node_source`: Xác định tên nguồn vệ tinh đang báo cáo (Mặc định: `8000kicks`).
  * `target_controller`: Đường dẫn tuyệt đối của lõi điều khiển đích tiếp nhận tại Tổng trạm.
  * `timestamp`: Thời gian gửi gói tin theo chuẩn định dạng UTC quốc tế.
  * `status`: Trạng thái hoạt động của Node (Mặc định: `NODE_ALIVE`).
  * `active_siphons`: Danh sách toàn bộ các tệp Python nghiệp vụ đang chạy song song tại vệ tinh.
  * `network_metadata`: Phiên bản cấu trúc mạng và giao thức định tuyến đang áp dụng.
---
### 🔄 4. TIẾN TRÌNH XỬ LÝ LÕI (OPERATIONAL LOGIC)
Tệp lệnh thực thi tuần tự theo chu kỳ vòng lặp khép kín:
1. **Giai đoạn 1: Thu nạp Quyền xác thực**
   * Tiến trình bóc tách biến `BRIDGE_TOKEN`. Nếu biến này trống, hệ thống bẻ gãy luồng chạy ngay lập tức nhằm ngăn chặn các yêu cầu gửi tin rác không hợp lệ lên Tổng trạm.
2. **Giai đoạn 2: Quét sơ đồ Mô-đun phụ trợ**
   * Hệ thống tự động kiểm tra sự tồn tại của thư mục nghiệp vụ, liệt kê các tệp cấu trúc có đuôi mở rộng dạng mã nguồn và loại trừ chính tệp cầu nối để lấy ra danh sách các mô-đun đang hoạt động.
3. **Giai đoạn 3: Phát xung lực phản hồi và Chống nghẽn mạch**
   * Thực hiện gọi giao thức mạng an toàn với thời gian chờ tối đa là **15 giây** cho mỗi lượt kết nối để tránh treo luồng máy chủ ảo.
   * Nếu trạng thái phản hồi trả về mã thành công (`200` hoặc `204`), hệ thống xác nhận thông tuyến trực tiếp với Drone Mesh Controller. Nếu thất bại, tiến trình tự động tạm dừng **3 giây** trước khi thử lại.
---
### 🚨 BIỆN PHÁP XỬ LÝ SỰ CỐ (TROUBLESHOOTING)
* **Lỗi Từ Chối Quyền (Mã lỗi 401/403/404):** Xuất hiện khi mã token ngắn hạn hết hiệu lực hoặc cấu hình quyền hạn liên kho tại Tổng trạm bị chặn. Cần kiểm tra lại cài đặt Token hệ thống tại Kho 4.
* **Lỗi Thất Bại Toàn Phần (Mesh Critical):** Xảy ra khi cả ba lần thử phát xung đều không thể thông tuyến. Đây là dấu hiệu của việc nghẽn mạng API cục bộ trên máy chủ GitHub hoặc sai lệch đường dẫn mục tiêu cấu hình trong tệp `KHO_4_REPO`.
