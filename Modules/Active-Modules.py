import json
import os
from datetime import datetime

def activate_all_modules():
    # Định vị thư mục Modules/ và Thư mục gốc dự án
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    
    # KHÓA CỨNG: Chỉ dùng đúng 1 file duy nhất ở gốc cho index.html đọc
    root_bridge_path = os.path.join(root_dir, "system_bridge.json")
    
    print("[+] KÍCH HOẠT NEURAL SIPHON PROTOCOL - QUÉT FILE MODULES...")
    detected_modules = {}
    
    # Quét tất cả các file .py trong thư mục Modules
    for item in os.listdir(current_dir):
        if item.endswith(".py") and item != "Active-Modules.py":
            module_name = item.replace(".py", "")
            detected_modules[module_name] = {
                "status": "ACTIVE_SOTA",
                "mode": "HYPER_INTELLIGENCE_2026",
                "pulse_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            }
            print(f" |-- [ONLINE] Module: {item} -> Đã nén tín hiệu.")

    # Đọc dữ liệu cũ cấu trúc gốc nếu có
    base_data = {}
    if os.path.exists(root_bridge_path):
        try:
            with open(root_bridge_path, "r", encoding="utf-8") as f:
                base_data = json.load(f)
        except Exception:
            pass

    # Đồng bộ trực tiếp ma trận module vào cấu trúc lõi
    base_data.update({
        "sync_status": "PULSING_RED",
        "recursive_singularity": "ACTIVE_SOTA",
        "core_constant": 0.24,
        "active_modules_matrix": detected_modules,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    })

    # Ghi đè duy nhất vào thư mục gốc
    with open(root_bridge_path, "w", encoding="utf-8") as f:
        json.dump(base_data, f, indent=4, ensure_ascii=False)
        
    print(f"[SUCCESS] Ma trận đã hợp nhất {len(detected_modules)} Modules vào system_bridge.json ở gốc!")

if __name__ == "__main__":
    activate_all_modules()
    
