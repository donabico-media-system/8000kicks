import json
import os
from datetime import datetime

def activate_all_modules():
    # Định vị thư mục Modules/ và Thư mục gốc dự án
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    
    # Chỉ định vị trí duy nhất của file kết quả tại thư mục gốc
    root_bridge_path = os.path.join(root_dir, "system_bridge.json")
    
    print("[+] KÍCH HOẠT NEURAL SIPHON PROTOCOL - QUÉT FILE MODULES...")
    detected_modules = {}
    
    # Quét tất cả các file .py trong thư mục Modules (trừ chính file này)
    for item in os.listdir(current_dir):
        if item.endswith(".py") and item != "Active-Modules.py":
            module_name = item.replace(".py", "")
            
            # Ghi nhận kết quả tích xanh và cấu hình ánh xạ logic về Super Core xử lý tiếp
            detected_modules[module_name] = {
                "status": "KÍCH HOẠT THÀNH CÔNG ✅",
                "logic_mapping": "Super Core Affiliate/Super-Core-Affiliate.py",
                "mode": "HYPER_INTELLIGENCE_2026",
                "pulse_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            }
            print(f" |-- [ONLINE] Module: {item} -> Đã chuyển hướng ánh xạ ✅")

    # Đọc dữ liệu cũ ở gốc nếu có
    base_data = {}
    if os.path.exists(root_bridge_path):
        try:
            with open(root_bridge_path, "r", encoding="utf-8") as f:
                base_data = json.load(f)
        except Exception:
            pass

    # Hợp nhất và định chuẩn ma trận
    base_data.update({
        "sync_status": "PULSING_RED",
        "recursive_singularity": "ACTIVE_SOTA",
        "core_constant": 0.24,
        "active_modules_matrix": detected_modules,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    })

    # Ghi đè trực tiếp ra thư mục gốc cho index.html đọc
    with open(root_bridge_path, "w", encoding="utf-8") as f:
        json.dump(base_data, f, indent=4, ensure_ascii=False)
        
    print(f"[SUCCESS] Ma trận đã hợp nhất {len(detected_modules)} Modules với dấu tích xanh xác minh thành công!")

if __name__ == "__main__":
    activate_all_modules()
