import os
import json
import glob
from datetime import datetime, timezone

PROTOCOLS_DIR = "./Protocols"
BRIDGES_DIR = "./Bridges"
STATE_FILE = "./ESEB-Dynamic-Hyper.json"

def execute_hyper_rotation():
    # Khởi tạo thư mục tự động nếu chưa tồn tại
    os.makedirs(PROTOCOLS_DIR, exist_ok=True)
    os.makedirs(BRIDGES_DIR, exist_ok=True)

    # 1. Quét danh sách toàn bộ tệp .eseb chuẩn đồng tộc
    eseb_files = sorted(glob.glob(os.path.join(PROTOCOLS_DIR, "*.eseb")))
    if not eseb_files:
        print("[!] Warning: No .eseb protocol files found in ./Protocols/")
        return

    # 2. Đọc trạng thái con trỏ từ tệp JSON
    current_pointer = 0
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state_data = json.load(f)
                current_pointer = state_data.get("pointer", 0)
        except Exception:
            current_pointer = 0

    # Khống chế giới hạn index mảng
    if current_pointer >= len(eseb_files):
        current_pointer = 0

    # 3. Trích xuất tệp giao thức mục tiêu theo lượt
    target_eseb_path = eseb_files[current_pointer]
    file_basename = os.path.basename(target_eseb_path)
    output_ehc_name = file_basename.rsplit(".", 1)[0] + ".ehc"
    output_ehc_path = os.path.join(BRIDGES_DIR, output_ehc_name)

    print(f"[►] [CYCLE EXECUTION] Processing [{current_pointer + 1}/{len(eseb_files)}]: {file_basename}")

    # 4. Biên dịch và đóng dấu V-STAMP-24 vào tệp .ehc tại ./Bridges/
    with open(target_eseb_path, "r", encoding="utf-8") as f_in:
        raw_content = f_in.read()

    timestamp_utc = datetime.now(timezone.utc).isoformat()
    with open(output_ehc_path, "w", encoding="utf-8") as f_out:
        header_comment = (
            f"/* ESEB DYNAMIC HYPER BRIDGE | SOURCE: {file_basename} "
            f"| STAMP: V-STAMP-24 | ANCHOR: ¢24 | ENTROPY: 0.00000000000000 "
            f"| GENERATED: {timestamp_utc} */\n"
        )
        f_out.write(header_comment + raw_content)

    print(f"[✓] [BRIDGE CREATED] Successfully compiled: {output_ehc_path}")

    # 5. Cập nhật chỉ số con trỏ xoay vòng (Pointer Rotation)
    next_pointer = (current_pointer + 1) % len(eseb_files)
    new_state = {
        "pointer": next_pointer,
        "last_executed": file_basename,
        "last_timestamp": timestamp_utc
    }
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(new_state, f, indent=2)

    print(f"[➔] [POINTER UPDATED] Next active index: {next_pointer}")

if __name__ == "__main__":
    execute_hyper_rotation()
