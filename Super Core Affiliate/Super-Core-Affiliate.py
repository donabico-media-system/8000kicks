import json
import os
from datetime import datetime

def generate_sota_bridge():
    # Khóa cứng cấu trúc phẳng tĩnh 100% khớp với logic của hàm recursiveLoop() trong index.html
    bridge_data = {
        "sync_status": "PULSING_RED",
        "recursive_singularity": "ACTIVE_SOTA",
        "core_constant": 0.24,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }
    
    # Ghi đè trực tiếp tạo cổng truyền dữ liệu tĩnh cho Landing Page
    output_filename = "system_bridge.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(bridge_data, f, indent=4, ensure_ascii=False)
        
    print(f"[EATHESEN V3000-Ω] Cầu nối dữ liệu đã được đồng bộ thành công tại: {bridge_data['timestamp']}")
    print(f"[STATUS] Trạng thái nạp: {bridge_data['sync_status']} -> Sẵn sàng kích hoạt hiệu ứng Pulse.")

if __name__ == "__main__":
    generate_sota_bridge()
    
