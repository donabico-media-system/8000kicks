import os
import json
import sys
import time
import requests

# Khai báo Biến Môi trường
FINE_TOKEN = os.getenv("ESEB_FINE_TOKEN")
CLASSIC_TOKEN = os.getenv("ESEB_CLASSIC_TOKEN")
ORG_NAME = os.getenv("PRIMARY_ORG", "donabico-global-media")
TARGET_INPUT = os.getenv("TARGET_REPO_INPUT", "ALL")

# Danh sách các Kho Vệ tinh trong Hệ sinh thái DONABICO GLOBAL MEDIA
SATELLITE_REPOS = [
    "KHO-1-V3000-OMEGA-SOTA",
    "KHO-2-V3000-OMEGA-SOTA",
    "KHO-4-DRONE-LANDING-PAGE-CONTROL-CENTER",
    "8000kicks"
]

def update_internal_state():
    """Tác vụ 1: Dùng FINE_TOKEN cập nhật dữ liệu nội bộ."""
    print("🔄 [FINE_TOKEN] Đang làm mới dữ liệu trạng thái ESEB nội bộ...")
    state_payload = {
        "anchor": "¢24",
        "stamp": "V-STAMP-24-SOTA",
        "timestamp": int(time.time()),
        "status": "ACTIVE_PULSE_STABLE"
    }
    
    os.makedirs("./code-snippets", exist_ok=True)
    with open("./code-snippets/ESEB-Dynamic-Hyper.json", "w", encoding="utf-8") as f:
        json.dump(state_payload, f, indent=2, ensure_ascii=False)
    print("✅ [FINE_TOKEN] Đã cập nhật file ESEB-Dynamic-Hyper.json thành công.")

def dispatch_cross_repo_signal(repo_name):
    """Tác vụ 2: Dùng CLASSIC_TOKEN phát tín hiệu liên thông sang kho khác."""
    url = f"https://api.github.com/repos/{ORG_NAME}/{repo_name}/dispatches"
    headers = {
        "Authorization": f"Bearer {CLASSIC_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    payload = {
        "event_type": "FORCE_ESEB_ROTATE",
        "client_payload": {
            "source": "MASTER-ECOSYSTEM-V3000",
            "anchor": "¢24",
            "timestamp": int(time.time())
        }
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        if res.status_code == 204:
            print(f"🚀 [CLASSIC_TOKEN] Bắn tín hiệu thành công tới kho: {repo_name}")
        else:
            print(f"⚠️ [CLASSIC_TOKEN] Thất bại tại kho {repo_name} | HTTP {res.status_code}: {res.text}")
    except Exception as e:
        print(f"❌ Lỗi kết nối tới kho {repo_name}: {str(e)}")

def main():
    if not FINE_TOKEN or not CLASSIC_TOKEN:
        print("❌ LỖI BẢO MẬT: Chưa cấu hình đủ ESEB_FINE_TOKEN hoặc ESEB_CLASSIC_TOKEN trong Secrets!")
        sys.exit(1)

    # 1. Thực thi nội bộ
    update_internal_state()

    # 2. Phát tín hiệu Đa kho (Cascade Broadcast)
    print("\n📡 [CASCADE ENGINE] Bắt đầu kích hoạt sóng tín hiệu liên thông...")
    if TARGET_INPUT == "ALL":
        for repo in SATELLITE_REPOS:
            dispatch_cross_repo_signal(repo)
    else:
        dispatch_cross_repo_signal(TARGET_INPUT)

if __name__ == "__main__":
    main()
