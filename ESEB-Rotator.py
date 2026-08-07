import os
import json
import sys
import time
import requests

# Khai báo Biến Môi trường từ Workflow
CLASSIC_TOKEN = os.getenv("ESEB_CLASSIC_TOKEN")
ORG_NAME = os.getenv("PRIMARY_ORG", "donabico-media-system")
TARGET_INPUT = os.getenv("TARGET_REPO_INPUT", "ALL")

# Danh sách các Kho Vệ tinh trong Mạng lưới Ecosystem DONABICO
SATELLITE_REPOS = [
    "KHO-1-V3000-OMEGA-SOTA",
    "KHO-2-V3000-OMEGA-SOTA",
    "KHO-4-DRONE-LANDING-PAGE-CONTROL-CENTER",
    "8000kicks"
]

def update_internal_eseb_state():
    """Tác vụ 1: Cập nhật state dữ liệu xoay vòng ESEB tại kho hiện tại."""
    print("🔄 [CLASSIC_ENGINE] Đang khởi tạo dữ liệu ESEB Dynamic Hyper...")
    
    current_timestamp = int(time.time())
    state_payload = {
        "engine": "EATHESEN-V3000-SOTA",
        "anchor": "¢24",
        "stamp": f"STAMP-EATHESEN-{current_timestamp}",
        "last_sync": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "status": "ACTIVE_PULSE_STABLE"
    }
    
    output_dir = "./code-snippets"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "ESEB-Dynamic-Hyper.json")
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(state_payload, f, indent=2, ensure_ascii=False)
        
    print(f"✅ [CLASSIC_ENGINE] Đã lưu thành công dữ liệu mới tại: {file_path}")

def dispatch_cross_repo_signal(target_repo):
    """Tác vụ 2: Tận dụng Classic Token phát tín hiệu liên thông Đa kho."""
    url = f"https://api.github.com/repos/{ORG_NAME}/{target_repo}/dispatches"
    headers = {
        "Authorization": f"Bearer {CLASSIC_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    payload = {
        "event_type": "FORCE_ESEB_ROTATE",
        "client_payload": {
            "source": "EATHESEN-MASTER-ECOSYSTEM",
            "anchor": "¢24",
            "timestamp": int(time.time())
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 204:
            print(f"🚀 [CASCADE DISPATCH] Bắn tín hiệu thành công tới kho: {target_repo}")
        else:
            print(f"⚠️ [DISPATCH FAILED] Kho {target_repo} trả về lỗi HTTP {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Lỗi kết nối API tới kho {target_repo}: {str(e)}")

def main():
    if not CLASSIC_TOKEN:
        print("❌ LỖI BẢO MẬT BẮT BUỘC: Chưa khai báo ESEB_CLASSIC_TOKEN trong Repository Secrets!")
        sys.exit(1)

    print("=== KÍCH HOẠT HỆ THỐNG ESEB DYNAMIC HYPER (CLASSIC TOKEN FULL SCOPE) ===")
    
    # 1. Xử lý lưu state nội bộ
    update_internal_eseb_state()

    # 2. Phát tín hiệu xoay vòng liên thông sang các kho vệ tinh
    print("\n📡 [CASCADE BROADCAST] Đang phát sóng điều khiển đa kho...")
    if TARGET_INPUT == "ALL":
        for repo in SATELLITE_REPOS:
            dispatch_cross_repo_signal(repo)
    else:
        dispatch_cross_repo_signal(TARGET_INPUT)

    print("\n✅ Hoàn tất tiến trình vận hành ESEB Rotator!")

if __name__ == "__main__":
    main()
