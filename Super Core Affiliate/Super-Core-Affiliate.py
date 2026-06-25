import json
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# --- LOGIC CŨ CỦA ADMIN: GIỮ NGUYÊN BẢN 100% ---
def generate_sota_bridge():
    bridge_data = {
        "sync_status": "PULSING_RED",
        "recursive_singularity": "ACTIVE_SOTA",
        "core_constant": 0.24,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }
    
    output_filename = "system_bridge.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(bridge_data, f, indent=4, ensure_ascii=False)
        
    print(f"[EATHESEN V3000-Ω] Cầu nối dữ liệu đã được đồng bộ thành công tại: {bridge_data['timestamp']}")
    print(f"[STATUS] Trạng thái nạp: {bridge_data['sync_status']} -> Sẵn sàng kích hoạt hiệu ứng Pulse.")

# ==================== CÔNG NGHỆ THU THẬP SOTA MỚI ====================

class SuperCoreTransceiverHandler(BaseHTTPRequestHandler):
    """
    Bộ xử lý tín hiệu thông minh: Hứng, bóc tách và phân tích dữ liệu
    Telemetry từ Landing Page đẩy về thời gian thực.
    """
    def _set_headers(self):
        # Thiết lập CORS Header để Landing Page từ GitHub Pages thoải mái đẩy dữ liệu về Core không bị chặn
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        # Phản hồi các yêu cầu kiểm tra cổng (Preflight requests) từ trình duyệt
        self._set_headers()

    def do_POST(self):
        # Càn quét dữ liệu payload từ luồng Fetch / SendBeacon gửi về
        if self.path == '/api/v1/super-core-analytics':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Giải mã luồng dữ liệu JSON
                payload = json.loads(post_data.decode('utf-8'))
                event_type = payload.get("event_type", "UNKNOWN_SIGNAL")
                metrics = payload.get("metrics", {})
                session_id = metrics.get("session_id", "ANONYMOUS")
                
                print(f"\n⚡ [SIGNAL DETECTED] [{datetime.now().strftime('%H:%M:%S')}] Event: {event_type}")
                print(f"├── Session ID : {session_id}")
                print(f"├── Time On Page: {metrics.get('time_on_page')}s | Scroll Depth: {metrics.get('max_scroll_depth')}%")
                print(f"├── Click Count : {metrics.get('click_count')} | Exit Intent: {metrics.get('exit_intent_triggered')}")
                
                if metrics.get('last_clicked_element'):
                    print(f"└── Last Clicked: {metrics['last_clicked_element'].get('text')} -> {metrics['last_clicked_element'].get('href')}")

                # --- ĐỊA BÀN XỬ LÝ DỮ LIỆU CỦA CORE ---
                # Tại đây, dữ liệu 'metrics' đã nằm gọn trong bộ nhớ Python. 
                # Anh có thể viết thêm logic chấm điểm ROI hoặc lưu file log tùy ý.

                # Phản hồi trạng thái xử lý thành công về phía Client
                self._set_headers()
                response = {"status": "SUCCESS", "core_constant": 0.24, "signal_received": event_type}
                self.wfile.write(json.dumps(response).encode('utf-8'))

            except Exception as e:
                self.send_response(400)
                self.end_headers()
                print(f"[-] Lỗi bóc tách tín hiệu: {str(e)}")
        else:
            self.send_response(404)
            self.end_headers()

    # Chặn log mặc định của http.server để màn hình Console của Admin sạch sẽ nhất
    def log_message(self, format, *args):
        return

def start_core_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SuperCoreTransceiverHandler)
    print(f"\n[SOTA SERVER] Khởi chạy luồng thu thập ngầm tại cổng: {port}")
    print(f"[SHIELD] Cơ chế CORS Bypass chủ động - Sẵn sàng nhận Signal toàn cầu.")
    httpd.serve_forever()

if __name__ == "__main__":
    # 1. Chạy hàm sinh cầu nối tĩnh nguyên bản của anh
    generate_sota_bridge()
    
    # 2. Tách luồng (Threading): Kích hoạt máy chủ hứng tín hiệu ngầm, không block tiến trình chính
    server_thread = threading.Thread(target=start_core_server, args=(8080,), daemon=True)
    server_thread.start()
    
    # 3. Giữ cho Script chạy liên tục để duy trì Server
    print("\n[EATHESEN V3000-Ω] ĐÃ THIẾT LẬP MA TRẬN PHÂN TÍCH HAI CHIỀU THÀNH CÔNG.")
    print("Môi trường đang lắng nghe tín hiệu... Bấm Ctrl+C để dừng.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[EATHESEN] Đang đóng hệ thống an toàn.")
