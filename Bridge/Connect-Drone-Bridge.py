import os
import sys
import time
import requests
from datetime import datetime

# --- CẤU HÌNH ĐỊNH TUYẾN MẠNG LƯỚI ---
KHO_4_REPO = "donabico-global-media/KHO-4-DRONE-LANDING-PAGE-CONTROL-CENTER"
KHO_4_DISPATCH_ENDPOINT = f"https://api.github.com/repos/{KHO_4_REPO}/dispatches"

# Đường dẫn mục tiêu xử lý trên Tổng trạm Kho 4
TARGET_MESH_CONTROLLER = "Protocol/Connet Affiliate Drone/Drone_Mesh_Controller.py"
NODE_SOURCE_NAME = "8000kicks"

def establish_mesh_connection():
    """
    Khởi tạo kết nối trực tiếp từ Node Vệ tinh về Lõi Mesh Controller tại Tổng trạm Kho 4.
    """
    print(f"[MESH-BRIDGE] 📡 Đang khởi động cổng kết nối nội bộ...")
    print(f"[MESH-BRIDGE] Đích đến: Kho 4 -> {TARGET_MESH_CONTROLLER}")

    # Thu nạp Token động từ luồng bảo mật mã hóa (Đảm bảo Zero-Secret cho Kho 8000kicks)
    bridge_token = os.getenv("BRIDGE_TOKEN")
    
    if not bridge_token:
        print("[❌ MESH-BRIDGE ERROR] Quyền truy cập bị từ chối: Không tìm thấy 'BRIDGE_TOKEN'.")
        print("[💡 GỢI Ý] Tệp lệnh này phải được kích hoạt từ Workflow nhận tín hiệu ký gửi")
        print("           hoặc được cấp mã xác thực ngắn hạn từ Tổng trạm Kho 4 truyền sang.")
        sys.exit(1)

    # Tự động quét và liệt kê danh sách các module siphon phụ trợ đang hoạt động tại Node vệ tinh
    active_siphons = []
    try:
        if os.path.exists("Modules"):
            active_siphons = [f for f in os.listdir("Modules") if f.endswith(".py") and f != "Connect-Drone-Bridge.py"]
            print(f"[MESH-BRIDGE] Phát hiện các Module vệ tinh đang chạy: {active_siphons}")
    except Exception as e:
        print(f"[⚠️ WARNING] Cảnh báo quét danh mục cấu trúc thất bại: {e}")

    # Đóng gói gói tin Mesh Node Payload định dạng tiêu chuẩn cho Drone_Mesh_Controller.py tiếp nhận
    payload = {
        "event_type": "DRONE_MESH_CONNECT",
        "client_payload": {
            "node_source": NODE_SOURCE_NAME,
            "target_controller": TARGET_MESH_CONTROLLER,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "NODE_ALIVE",
            "active_siphons": active_siphons,
            "network_metadata": {
                "bridge_version": "V3000-Ω-Mesh-Node-002",
                "routing_protocol": "Direct-Repository-Dispatch-Mesh"
            }
        }
    }

    headers = {
        "Authorization": f"token {bridge_token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }

    # Thực hiện bắn tín hiệu xuyên màng lọc API với cơ chế chống nghẽn mạch
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"[📡 TRANSMIT] Đang phát xung tín hiệu về Tổng trạm Kho 4 (Lần thử {attempt + 1})...")
            response = requests.post(KHO_4_DISPATCH_ENDPOINT, json=payload, headers=headers, timeout=15)
            
            if response.status_code in (200, 204):
                print("✅ [MESH-BRIDGE] THÔNG TUYẾN THÀNH CÔNG TRỰC TIẾP VỚI DRONE MESH CONTROLLER!")
                print(f"[SYSTEM] Tín hiệu đồng bộ nạp vào Kho 4 hoàn tất lúc: {datetime.utcnow()} UTC.")
                return True
            else:
                print(f"[⚠️ MESH-BRIDGE] Tổng trạm phản hồi trạng thái lạ: {response.status_code}")
                print(f"Chi tiết phản hồi: {response.text}")
        except Exception as e:
            print(f"[❌ MESH-BRIDGE LỖI] Đường truyền gián đoạn ở lần thử {attempt + 1}: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(3)

    print("[❌ MESH-BRIDGE CRITICAL] Toàn bộ các lần phát xung kết nối về Mesh Controller đều thất bại.")
    return False

if __name__ == "__main__":
    establish_mesh_connection()
