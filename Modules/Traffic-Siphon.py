#!/usr/bin/env python3
import argparse
import json
import urllib.request
import urllib.error
import os
from datetime import datetime, timezone

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=False)
    args = parser.parse_args()
    
    # URL mặc định của hệ thống
    target_url = args.url if args.url else "https://donabico-global-media.github.io/8000kicks/"
    
    # GIẢI PHÁP: Ghi trực tiếp tại thư mục hiện hành vì Workflow đã thực hiện 'cd Modules'
    report_path = "traffic_report.json"
    
    history = []
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            try: 
                history = json.load(f)
            except Exception: 
                history = []

    # Thực hiện quét kiểm tra trạng thái HTTP
    try:
        with urllib.request.urlopen(target_url, timeout=10) as response:
            status = response.status
            message = "SUCCESS"
    except urllib.error.HTTPError as e:
        status = e.code
        message = "HTTP_ERROR"
    except Exception as e:
        status = 0
        message = str(e)[:30]

    # Đóng gói dữ liệu Telemetry chuẩn cấu trúc
    history.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "url": target_url,
        "status": status,
        "message": message
    })
    
    with open(report_path, "w") as f:
        json.dump(history, f, indent=4)
        
    print(f"[V3000-Ω] Traffic-Siphon thực thi thành công. Trạng thái phản hồi: {status}")

if __name__ == "__main__":
    main()
