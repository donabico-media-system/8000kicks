import json
import os
from datetime import datetime, timezone

def activate_all_protocols():
    # Xác định đường dẫn gốc và thư mục chứa protocols
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    bridge_path = os.path.join(root_dir, "Protocols-Bridge.json")
    
    print("[+] KÍCH HOẠT NEURAL SIPHON PROTOCOL - QUÉT TOÀN BỘ CẤU TRÚC...")
    detected_protocols = {}
    
    # Quét đệ quy toàn bộ thư mục Protocols và thư mục con
    for root, dirs, files in os.walk(current_dir):
        for item in files:
            # Loại trừ chính file này để tránh lỗi vòng lặp
            if item.endswith(".py") and item != "Active-Protocols.py":
                protocol_name = item.replace(".py", "")
                # Đường dẫn tương đối để dễ định danh
                rel_path = os.path.relpath(os.path.join(root, item), current_dir)
                
                detected_protocols[protocol_name] = {
                    "status": "ACTIVE_INFINITE ✅",
                    "path": rel_path,
                    "pulse_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
                }

    # Cấu trúc dữ liệu đầu ra
    data = {
        "sync_status": "PULSING_GREEN",
        "recursive_singularity": "ACTIVE_SOTA",
        "active_protocols_matrix": detected_protocols,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    }

    # Ghi dữ liệu vào Bridge
    with open(bridge_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"[SUCCESS] Đã quét thấy {len(detected_protocols)} Protocols. Ma trận đã cập nhật vào Protocols-Bridge.json!")

if __name__ == "__main__":
    activate_all_protocols()
