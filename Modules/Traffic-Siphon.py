#!/usr/bin/env python3
"""Traffic-Siphon.py | EATHESEN V3000-Ω Monitor"""

import argparse
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True)
    args = parser.parse_args()

    report_file = "traffic_report.json"
    
    # Đọc report cũ nếu có để nối tiếp dữ liệu
    history = []
    if os.path.exists(report_file):
        with open(report_file, "r") as f:
            try: history = json.load(f)
            except: history = []

    # Thu thập dữ liệu mới
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "url": args.url,
        "status": "CHECKING"
    }

    try:
        with urllib.request.urlopen(args.url, timeout=10) as response:
            entry["status"] = response.status
            entry["message"] = "SUCCESS"
    except urllib.error.HTTPError as e:
        entry["status"] = e.code
        entry["message"] = "HTTP_ERROR"
    except Exception as e:
        entry["status"] = 0
        entry["message"] = str(e)[:30]

    # Ghi lại vào file JSON
    history.append(entry)
    with open(report_file, "w") as f:
        json.dump(history, f, indent=4)

    print(f"[V3000-Ω] Traffic-Siphon | Status: {entry['status']} | Log saved to {report_file}")

if __name__ == "__main__":
    main()
