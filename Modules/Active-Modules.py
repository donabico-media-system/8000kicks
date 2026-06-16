#!/usr/bin/env python3
"""
Active-Modules.py
EATHESEN V3000-Ω | Active Modules Orchestrator
Kho Thương Hiệu 8000Kicks
Chức năng: Tự động kích hoạt toàn bộ các Module trong thư mục Modules (vô hạn)
Chu kỳ: Mỗi 30 phút
V-STAMP 24 AUTHENTICATED | ¢24 IMMUTABLE | BIÊN HÒA 2026
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


def get_all_modules() -> list[Path]:
    """Lấy danh sách tất cả file .py trong thư mục Modules (trừ file bị loại trừ)"""
    modules = []
    for file in MODULES_DIR.glob("*.py"):
        if file.name not in EXCLUDE_FILES:
            modules.append(file)
    return sorted(modules)


def run_module(module_path: Path) -> dict:
    """Chạy một module bằng subprocess"""
    result = {
        "module": module_path.name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "FAILED",
        "returncode": None,
        "error": None,
    }
    try:
        print(f"\n[ACTIVE] Đang kích hoạt: {module_path.name}")
        process = subprocess.run(
            [sys.executable, str(module_path)],
            capture_output=True,
            text=True,
            timeout=300,  # timeout 5 phút cho mỗi module
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
    print(f"[TIME] {datetime.now(timezone.utc).isoformat()}")
    print(f"[CYCLE] Mỗi {SLEEP_SECONDS // 60} phút")
    print("=" * 70)

    while True:
        modules = get_all_modules()
        print(f"\n[SCAN] Phát hiện {len(modules)} module(s) tại {MODULES_DIR}")

        for module in modules:
            run_module(module)
            time.sleep(3)  # Nghỉ ngắn giữa các module

        print(f"\n[COMPLETE] Đã kích hoạt xong toàn bộ module. Ngủ {SLEEP_SECONDS // 60} phút...")
        time.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    main()
