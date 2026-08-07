/* =================================================================================
   ESEB DYNAMIC HYPER ROTATOR ENGINE - QUAD-SECRET INTEGRATION
   BRAND: DONABICO GLOBAL MEDIA SYSTEM | SYSTEM: EATHESEN
   STAMP: V-STAMP-24 | ANCHOR: ¢24 | ENTROPY DELTA: 0.00000000000000
   ================================================================================= */

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

# ENDPOINTS DỊCH VỤ API
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
NVIDIA_ENDPOINT = "https://integrate.api.nvidia.com/v1/chat/completions"

PROTOCOLS_DIR = "./Protocols"
BRIDGES_DIR = "./Bridges"
STATE_FILE = "./ESEB-Dynamic-Hyper.json"

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

def execute_hyper_rotation():
    eseb_files = sorted(glob.glob(os.path.join(PROTOCOLS_DIR, "*.eseb")))
    if not eseb_files:
        print("[!] Warning: No .eseb protocol files found in Protocols/")
        return

    current_pointer = 0
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
    output_ehc_name = file_basename.rsplit(".", 1)[0] + ".ehc"
    output_ehc_path = os.path.join(BRIDGES_DIR, output_ehc_name)

    print(f"[►] [CYCLE EXECUTION] Processing [{current_pointer + 1}/{len(eseb_files)}]: {file_basename}")

    os.makedirs(BRIDGES_DIR, exist_ok=True)
    with open(target_eseb_path, "r", encoding="utf-8") as f_in:
        raw_content = f_in.read()

    # KÍCH HOẠT BIÊN DỊCH BỞI TỨ TRỤ API
    ai_compiled_code = compile_with_quad_pipeline(raw_content)
    final_payload = ai_compiled_code if ai_compiled_code else raw_content

    with open(output_ehc_path, "w", encoding="utf-8") as f_out:
        header_comment = f"/* ESEB DYNAMIC HYPER BRIDGE | SOURCE: {file_basename} | STAMP: V-STAMP-24 | GENERATED: {datetime.now(timezone.utc).isoformat()} */\n"
        f_out.write(header_comment + final_payload)

    print(f"[✓] [BRIDGE CREATED] Successfully compiled: {output_ehc_path}")

    next_pointer = (current_pointer + 1) % len(eseb_files)
    new_state = {
        "pointer": next_pointer,
        "last_executed": file_basename,
        "last_timestamp": datetime.now(timezone.utc).isoformat()
    }
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(new_state, f, indent=2)

    print(f"[➔] [POINTER UPDATED] Next active index: {next_pointer}")

if __name__ == "__main__":
    execute_hyper_rotation()
