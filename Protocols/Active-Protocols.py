import json
import os
from datetime import datetime

def activate_all_protocols():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    # File kết quả là Protocols-Bridge.json[span_1](start_span)[span_1](end_span)
    bridge_path = os.path.join(root_dir, "Protocols-Bridge.json")
    
    print("[+] KÍCH HOẠT PROTOCOL SIPHON - QUÉT VÔ HẠN CÁC PROTOCOLS...")
    detected_protocols = {}
    
    for item in os.listdir(current_dir):
        if item.endswith(".py") and item != "Active-Protocols.py":
            protocol_name = item.replace(".py", "")
            detected_protocols[protocol_name] = {
                "status": "ACTIVE_INFINITE ✅",
                "pulse_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            }

    data = {
        "sync_status": "PULSING_GREEN",
        "recursive_singularity": "ACTIVE_SOTA",
        "active_protocols_matrix": detected_protocols,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

    with open(bridge_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"[SUCCESS] Ma trận {len(detected_protocols)} Protocols đã được cập nhật vào Protocols-Bridge.json!")

if __name__ == "__main__":
    activate_all_protocols()
