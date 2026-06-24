import os
import sys
import time
import requests
from datetime import datetime

# --- ĐỒNG BỘ HÓA TỌA ĐỘ ĐÍCH CHUẨN XÁC THEO CHỈ THỊ ---
KHO_4_REPO = "donabico-global-media/KHO-4-DRONE-LANDING-PAGE-CONTROL-CENTER"
KHO_4_DISPATCH_ENDPOINT = f"https://api.github.com/repos/{KHO_4_REPO}/dispatches"

TARGET_MESH_CONTROLLER = "Protocol/Connet Affiliate Drone/Drone_Mesh_Controller.py"
NODE_SOURCE_NAME = "8000kicks"

def establish_mesh_connection():
    print(f"[MESH-BRIDGE] 📡 Đang khởi động cổng kết nối nội bộ...")
    print(f"[MESH-BRIDGE] Đích đến: Kho 4 -> {TARGET_MESH_CONTROLLER}")

    # Rút mã Token động từ môi trường Workflow bảo mật
    bridge_token = os.getenv("BRIDGE_TOKEN")
    
    if not bridge_token:
        print("[❌ MESH-BRIDGE ERROR] Quyền truy cập bị từ chối: Không tìm thấy 'BRIDGE_TOKEN'.")
        return False

    payload = {
        "event_type": "LAUNCH_DRONE_MESH_CONNECT",
        "client_payload": {
            "satellite_node": NODE_SOURCE_NAME,
            "timestamp": datetime.utcnow().isoformat(),
            "active_modules": [
                'Performance-Max.py', 'Affiliate-Network-Siphon.py', 'Filter-BotAI.py', 
                'Push-To-Google-Ads.py', 'Drone-Matrix.py', 'Bing-Siphon.py', 
                'Seo-Optimizer.py', 'ADTech-Traffic.py', 'AI-Cache-Siphon.py', 
                'SEO-Shield-Siphon.py', 'Social-Preview-Siphon.py', 'Google-Siphon.py', 
                'Active-Modules.py'
            ],
            "telemetry": {
                "status": "HEALTHY",
                "bridge_version": "V3000-OMEGA",
                "mesh_node_id": "DNBC-Mesh-Node-002",
                "routing_protocol": "Direct-Repository-Dispatch-Mesh"
            }
        }
    }

    headers = {
        "Authorization": f"token {bridge_token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"[📡 TRANSMIT] Đang phát xung tín hiệu về Tổng trạm Kho 4 (Lần thử {attempt + 1})...")
            response = requests.post(KHO_4_DISPATCH_ENDPOINT, json=payload, headers=headers, timeout=15)
            
            if response.status_code in (200, 204):
                print("✅ [MESH-BRIDGE] THÔNG TUYẾN THÀNH CÔNG TRỰC TIẾP VỚI DRONE MESH CONTROLLER!")
                return True
            else:
                print(f"[⚠️ MESH-BRIDGE] Tổng trạm phản hồi trạng thái lạ: {response.status_code}")
                print(f"Chi tiết phản hồi: {response.text}")
        except Exception as e:
            print(f"[❌ MESH-BRIDGE LỖI] Đường truyền gián đoạn ở lần thử {attempt + 1}: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(2)
            
    print("[❌ MESH-BRIDGE CRITICAL] Toàn bộ các lần phát xung kết nối đều thất bại.")
    return False

if __name__ == "__main__":
    success = establish_mesh_connection()
    if not success:
        sys.exit(1)
        
