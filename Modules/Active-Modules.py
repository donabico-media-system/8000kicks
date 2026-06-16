#!/usr/bin/env python3
"""
Active-Modules.py
EATHESEN V3000-Ω | Active Modules Orchestrator (Infinite Scalability Update)
"""

import os
import sys
import time
import subprocess
from datetime import datetime, timezone
from pathlib import Path

MODULES_DIR = Path(__file__).parent
EXCLUDE_FILES = {"Active-Modules.py", "__init__.py"}
SLEEP_SECONDS = 30 * 60  # 30 phút

# Tự động bắt tọa độ từ Workflow, nếu chạy tay thì lấy tọa độ dự phòng
TARGET_URL = os.getenv("TARGET_AFFILIATE_URL", "https://donabico-global-media.github.io/8000kicks")

def get_all_modules() -> list[Path]:
    modules = []
    for file in MODULES_DIR.glob("*.py"):
        if file.name not in EXCLUDE_FILES:
            modules.append(file)
    return sorted(modules)

def run_module(module_path: Path) -> dict:
    result = {
        "module": module_path.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "FAILED",
        "returncode": None,
        "error": None,
    }
    try:
        print(f"\n[ACTIVE] Đang kích hoạt: {module_path.name}")
        # Truyền cờ --url chứa tọa độ xuống thẳng Module con
        process = subprocess.run(
            [sys.executable, str(module_path), "--url", TARGET_URL],
            capture_output=True,
            text=True,
            timeout=300,
        )
        result["returncode"] = process.returncode
        result["status"] = "SUCCESS" if process.returncode == 0 else "FAILED"
        
        if process.stdout:
            print(process.stdout.strip())
        if process.stderr:
            print(f"[STDERR] {process.stderr.strip()}")
            
    except subprocess.TimeoutExpired:
        result["error"] = "Timeout sau 5 phút"
    except Exception as e:
        result["error"] = str(e)
    
    print(f"[RESULT] {module_path.name} → {result['status']}")
    return result

def main():
    print("=" * 70)
    print(f"[EATHESEN V3000-Ω] ACTIVE-MODULES ORCHESTRATOR STARTED")
    print(f"[TARGET URL] {TARGET_URL}")
    print(f"[TIME] {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    # Chạy 1 vòng duy nhất trong GitHub Actions, vòng lặp vô hạn do cron job của file YAML lo liệu
    modules = get_all_modules()
    print(f"\n[SCAN] Phát hiện {len(modules)} module(s) tại {MODULES_DIR}")

    for module in modules:
        run_module(module)
        time.sleep(3)

    print(f"\n[COMPLETE] Đã kích hoạt xong toàn bộ module.")

if __name__ == "__main__":
    main()
