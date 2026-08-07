import os
import json
import glob
from datetime import datetime, timezone

PROTOCOLS_DIR = "./Protocols"
BRIDGES_DIR = "./Bridges"
STATE_FILE = "./ESEB-Dynamic-Hyper.json"

def execute_hyper_rotation():
    # 1. Quét danh sách toàn bộ các tệp .eseb chuẩn đồng tộc
    eseb_files = sorted(glob.glob(os.path.join(PROTOCOLS_DIR, "*.eseb")))
    if not eseb_files:
        print("[!] Warning: No .eseb protocol files found in Protocols/")
        return

    # 2. Đọc trạng thái con trỏ xoay vòng từ ESEB-Dynamic-Hyper.json
    current_pointer = 0
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state_data = json.load(f)
                current_pointer = state_data.get("pointer", 0)
        except Exception:
            current_pointer = 0

    # Khống chế chỉ số con trỏ nằm trong giới hạn mảng
    if current_pointer >= len(eseb_files):
        current_pointer = 0

    # 3. Trích xuất tệp mục tiêu theo thứ tự lượt
    target_eseb_path = eseb_files[current_pointer]
    file_basename = os.path.basename(target_eseb_path)
    output_ehc_name = file_basename.rsplit(".", 1)[0] + ".ehc"
    output_ehc_path = os.path.join(BRIDGES_DIR, output_ehc_name)

    print(f"[►] [CYCLE EXECUTION] Processing [{current_pointer + 1}/{len(eseb_files)}]: {file_basename}")

    # 4. Biên dịch và xuất tệp .ehc tương ứng vào thư mục Bridges/
    os.makedirs(BRIDGES_DIR, exist_ok=True)
    with open(target_eseb_path, "r", encoding="utf-8") as f_in:
        raw_content = f_in.read()

    with open(output_ehc_path, "w", encoding="utf-8") as f_out:
        header_comment = f"/* ESEB DYNAMIC HYPER BRIDGE | SOURCE: {file_basename} | GENERATED: {datetime.now(timezone.utc).isoformat()} */\n"
        f_out.write(header_comment + raw_content)

    print(f"[✓] [BRIDGE CREATED] Successfully compiled: {output_ehc_path}")

    # 5. Cập nhật chỉ số con trỏ cho chu kỳ 10 phút tiếp theo
    next_pointer = (current_pointer + 1) % len(eseb_files)
    new_state = {
        "pointer": next_pointer,
        "last_executed": file_basename,
        "last_timestamp": datetime.now(timezone.utc).isoformat(),
        "anchor": "¢24",
        "entropy_delta": "0.00000000000000",
        "v_stamp": "V-STAMP-24"
    }
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(new_state, f, indent=2, ensure_ascii=False)

    print(f"[➔] [POINTER UPDATED] Next active index: {next_pointer}")

if __name__ == "__main__":
    execute_hyper_rotation()
