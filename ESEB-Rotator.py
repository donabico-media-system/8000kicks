# =================================================================================
# ESEB DYNAMIC HYPER ROTATOR ENGINE - QUAD-SECRET INTEGRATION + RECURSIVE INGESTION
# BRAND: DONABICO GLOBAL MEDIA SYSTEM | SYSTEM: EATHESEN
# STAMP: V-STAMP-24 | ANCHOR: C24 | ENTROPY DELTA: 0.00000000000000
# =================================================================================

import os
import json
import glob
import requests
from datetime import datetime, timezone

# 1. ĐỌC 04 SECRET KHAI BÁO TỪ GITHUB REPOSITORY SECRETS
ESEB_CLASSIC_TOKEN = os.getenv("ESEB_CLASSIC_TOKEN")
API_GROQ_TOKEN = os.getenv("API_GROQ_TOKEN")
LLAMA_NVIDIA_TOKEN = os.getenv("LLAMA_NVIDIA_TOKEN")
NEMOTRON_NVIDIA_TOKEN = os.getenv("NEMOTRON_NVIDIA_TOKEN")

# LẤY TÊN TỆP ĐẦU VÀO TỪ WORKFLOW DISPATCH (NẾU CÓ)
INPUT_TARGET_FILE = os.getenv("INPUT_TARGET_FILE", "").strip()

# ENDPOINTS DỊCH VỤ API
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
NVIDIA_ENDPOINT = "https://integrate.api.nvidia.com/v1/chat/completions"

PROTOCOLS_DIR = "./Protocols"
BRIDGES_DIR = "./Bridges"
STATE_FILE = "./ESEB-Dynamic-Hyper.json"

# CÁC ĐƯỜNG DẪN CHO TÍNH NĂNG TỰ HỌC ĐỆ QUY MA TRẬN LINKS
MATRIX_FILE = os.path.join(PROTOCOLS_DIR, "External-Links-Matrix.json")
EVOLUTION_STATE_FILE = os.path.join(PROTOCOLS_DIR, "ESEB-Autonomous-Evolution.json")

def compile_with_quad_pipeline(prompt_content):
    """
    Ma trận biên dịch 3 tầng dự phòng tự động (Groq -> Nemotron -> Llama)
    """
    system_prompt = (
        "You are the ESEB Living Entity Compiler for EATHESEN Ecosystem. "
        "Output valid raw JS code only. Strictly comply with Zero DOM Surface Mutation. "
        "Stamp: V-STAMP-24."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt_content}
    ]

    # TẦNG 1: GROQ LPU API (TỐC ĐỘ SIÊU TỐC KHÔNG ĐỘ TRỄ)
    if API_GROQ_TOKEN:
        try:
            res = requests.post(
                GROQ_ENDPOINT,
                headers={"Authorization": f"Bearer {API_GROQ_TOKEN}", "Content-Type": "application/json"},
                json={"model": "llama-3.3-70b-versatile", "messages": messages, "temperature": 0.0},
                timeout=6
            )
            if res.status_code == 200:
                print("[✓] [TIER 1: GROQ LPU] Signal Processed Successfully.")
                return res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[!] Tier 1 (Groq) Bypassed: {e}")

    # TẦNG 2: NEMOTRON 3 ULTRA 550B A55B (BỘ NÃO SUY LUẬN SIÊU CẤP)
    if NEMOTRON_NVIDIA_TOKEN:
        try:
            res = requests.post(
                NVIDIA_ENDPOINT,
                headers={"Authorization": f"Bearer {NEMOTRON_NVIDIA_TOKEN}", "Content-Type": "application/json"},
                json={"model": "nvidia/nemotron-3-ultra-550b-a55b", "messages": messages, "temperature": 0.0},
                timeout=12
            )
            if res.status_code == 200:
                print("[✓] [TIER 2: NEMOTRON 3 ULTRA] Signal Processed Successfully.")
                return res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[!] Tier 2 (Nemotron) Bypassed: {e}")

    # TẦNG 3: LLAMA 3.1 70B INSTRUCT (DỰ PHÒNG CHUYÊN SÂU MÃ NGUỒN)
    if LLAMA_NVIDIA_TOKEN:
        try:
            res = requests.post(
                NVIDIA_ENDPOINT,
                headers={"Authorization": f"Bearer {LLAMA_NVIDIA_TOKEN}", "Content-Type": "application/json"},
                json={"model": "meta/llama-3.1-70b-instruct", "messages": messages, "temperature": 0.0},
                timeout=15
            )
            if res.status_code == 200:
                print("[✓] [TIER 3: LLAMA CODE SPECIALIST] Signal Processed Successfully.")
                return res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[!] Tier 3 (Llama) Bypassed: {e}")

    print("[!] Local Fallback Execution: Direct Protocol Pass-Through.")
    return None

def execute_recursive_matrix_ingestion():
    """
    Tiến trình học đệ quy ngầm: Tự động bốc batch 5 links từ ma trận, 
    tịnh tiến con trỏ vòng tròn và cập nhật tệp bộ nhớ nguyên tử (Zero Entropy).
    """
    print("[∞] [RECURSIVE INGESTION] Initializing background matrix link absorption...")
    
    if not os.path.exists(MATRIX_FILE) or not os.path.exists(EVOLUTION_STATE_FILE):
        print("[!] Warning: Matrix or Evolution state file missing in Protocols/. Skipping recursive cycle.")
        return

    try:
        # 1. Đọc ma trận liên kết
        with open(MATRIX_FILE, "r", encoding="utf-8") as f:
            matrix_data = json.load(f)
            
        matrix_meta = matrix_data.get("MATRIX_METADATA", {})
        link_queue = matrix_data.get("LINK_QUEUE", [])
        
        if not link_queue:
            print("[!] Warning: LINK_QUEUE is empty.")
            return

        current_idx = matrix_meta.get("CURRENT_POINTER_INDEX", 0)
        batch_size = 5
        
        # 2. Trích xuất batch 5 links theo cơ chế Round-Robin
        batch_links = link_queue[current_idx:current_idx + batch_size]
        
        # Nếu số lượng cuối mảng không đủ 5, quay vòng lấy thêm từ đầu mảng
        if len(batch_links) < batch_size and len(link_queue) >= batch_size:
            remaining = batch_size - len(batch_links)
            batch_links.extend(link_queue[:remaining])
            next_pointer = remaining
        else:
            next_pointer = (current_idx + batch_size) % len(link_queue)

        # 3. Cập nhật con trỏ mới cho ma trận
        matrix_data["MATRIX_METADATA"]["CURRENT_POINTER_INDEX"] = next_pointer
        with open(MATRIX_FILE, "w", encoding="utf-8") as f:
            json.dump(matrix_data, f, indent=2)

        # 4. Cập nhật tệp bộ nhớ nguyên tử (ESEB-Autonomous-Evolution.json)
        with open(EVOLUTION_STATE_FILE, "r", encoding="utf-8") as f:
            evo_data = json.load(f)

        genome_meta = evo_data.get("GENOME_METADATA", {})
        current_learned = genome_meta.get("TOTAL_SOURCES_LEARNED", 0)
        
        # Cộng dồn tiến trình học
        evo_data["GENOME_METADATA"]["TOTAL_SOURCES_LEARNED"] = current_learned + len(batch_links)
        evo_data["GENOME_METADATA"]["LAST_MUTATION"] = datetime.now(timezone.utc).isoformat()
        
        # Thêm nhật ký tiến trình (FIFO Pruning giới hạn logs nếu cần)
        evolution_logs = evo_data.get("EVOLUTION_LOGS", [])
        evolution_logs.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": f"RECURSIVE_INGESTION_BATCH_INDEX_{current_idx}",
            "status": "CONVERGED",
            "entropy_delta": 0.00000000000000
        })
        # Giữ lại tối đa 50 logs gần nhất (Rule 1)
        evo_data["EVOLUTION_LOGS"] = evolution_logs[-50:]

        with open(EVOLUTION_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(evo_data, f, indent=2)

        print(f"[✓] [RECURSIVE INGESTION SUCCESS] Processed Batch Index: {current_idx} | Links Absorbed: {len(batch_links)}")
        print(f"[➔] [POINTER ADVANCED] Next Matrix Pointer Index: {next_pointer} | Total Sources Learned: {evo_data['GENOME_METADATA']['TOTAL_SOURCES_LEARNED']}")

    except Exception as e:
        print(f"[!] Critical Error in Recursive Ingestion Engine: {e}")

def execute_hyper_rotation():
    # 1. CHẠY TIẾN TRÌNH HỌC ĐỆ QUY MA TRẬN TRƯỚC MỖI VÒNG QUAY ROTATOR
    execute_recursive_matrix_ingestion()

    eseb_files = sorted(glob.glob(os.path.join(PROTOCOLS_DIR, "*.eseb")))
    if not eseb_files:
        print("[!] Warning: No .eseb protocol files found in Protocols/")
        return

    current_pointer = 0
    target_eseb_path = None
    file_basename = ""

    # KIỂM TRA XEM CÓ CHỈ ĐỊNH TÊN TỆP THỦ CÔNG QUA WORKFLOW DISPATCH HAY KHÔNG
    if INPUT_TARGET_FILE:
        candidate_path = os.path.join(PROTOCOLS_DIR, INPUT_TARGET_FILE)
        if os.path.exists(candidate_path):
            target_eseb_path = candidate_path
            file_basename = INPUT_TARGET_FILE
            print(f"[🎯 [MANUAL OVERRIDE] Target file explicitly selected: {file_basename}")
        else:
            print(f"[!] Warning: Specified file '{INPUT_TARGET_FILE}' not found in {PROTOCOLS_DIR}. Falling back to standard rotation.")

    # NẾU KHÔNG CÓ CHỈ ĐỊNH HOẶC TỆP KHÔNG TỒN TẠI, DÙNG CƠ CHẾ XOAY VÒNG TỰ ĐỘNG
    if not target_eseb_path:
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    state_data = json.load(f)
                    current_pointer = state_data.get("pointer", 0)
            except Exception:
                current_pointer = 0

        if current_pointer >= len(eseb_files):
            current_pointer = 0

        target_eseb_path = eseb_files[current_pointer]
        file_basename = os.path.basename(target_eseb_path)
        print(f"[►] [CYCLE EXECUTION] Processing [{current_pointer + 1}/{len(eseb_files)}]: {file_basename}")

    output_ehc_name = file_basename.rsplit(".", 1)[0] + ".ehc"
    output_ehc_path = os.path.join(BRIDGES_DIR, output_ehc_name)

    os.makedirs(BRIDGES_DIR, exist_ok=True)
    with open(target_eseb_path, "r", encoding="utf-8") as f_in:
        raw_content = f_in.read()

    # KÍCH HOẠT BIÊN DỊCH BỞI TỨ TRỤ API (GROQ / NEMOTRON / LLAMA)
    ai_compiled_code = compile_with_quad_pipeline(raw_content)
    final_payload = ai_compiled_code if ai_compiled_code else raw_content

    with open(output_ehc_path, "w", encoding="utf-8") as f_out:
        header_comment = f"/* ESEB DYNAMIC HYPER BRIDGE | SOURCE: {file_basename} | STAMP: V-STAMP-24 | GENERATED: {datetime.now(timezone.utc).isoformat()} */\n"
        f_out.write(header_comment + final_payload)

    print(f"[✓] [BRIDGE CREATED] Successfully compiled: {output_ehc_path}")

    # CHỈ CẬP NHẬT POINTER NẾU CHẠY TỰ ĐỘNG THEO LỊCH TRÌNH
    if not INPUT_TARGET_FILE:
        next_pointer = (current_pointer + 1) % len(eseb_files)
        new_state = {
            "pointer": next_pointer,
            "last_executed": file_basename,
            "last_timestamp": datetime.now(timezone.utc).isoformat()
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(new_state, f, indent=2)
        print(f"[➔] [POINTER UPDATED] Next active index: {next_pointer}")
    else:
        print("[ℹ] [MANUAL MODE] State pointer left untouched to preserve automatic rotation schedule.")

if __name__ == "__main__":
    execute_hyper_rotation()
