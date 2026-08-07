import os
import json
import sys
import time
import requests

CLASSIC_TOKEN = os.getenv("ESEB_CLASSIC_TOKEN")
ORG_NAME = os.getenv("PRIMARY_ORG", "donabico-media-system")
TARGET_INPUT = os.getenv("TARGET_REPO_INPUT", "ALL")

# Điền danh sách tên repository THỰC TẾ của bạn vào đây (nếu có)
SATELLITE_REPOS = []

def update_internal_eseb_state():
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
    current_repo = os.getenv("GITHUB_REPOSITORY", "").split("/")[-1]
    if target_repo == current_repo:
        print(f"⏭️ Bỏ qua kho hiện tại ({target_repo}) để tránh tự lặp.")
        return

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
        elif response.status_code == 404:
            print(f"⚠️ [DISPATCH FAILED 404] Không tìm thấy kho '{target_repo}'!")
        else:
            print(f"⚠️ [DISPATCH FAILED] Kho {target_repo} trả về HTTP {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Lỗi kết nối API tới kho {target_repo}: {str(e)}")

def main():
    if not CLASSIC_TOKEN:
        print("❌ LỖI BẢO MẬT: Chưa khai báo ESEB_CLASSIC_TOKEN trong Secrets!")
        sys.exit(1)

    print("=== KÍCH HOẠT HỆ THỐNG ESEB DYNAMIC HYPER (CLASSIC TOKEN FULL SCOPE) ===")
    
    # 1. Cập nhật state nội bộ
    update_internal_eseb_state()

    # 2. Phát tín hiệu liên thông nếu có danh sách kho
    if SATELLITE_REPOS:
        print("\n📡 [CASCADE BROADCAST] Đang phát sóng điều khiển đa kho...")
        if TARGET_INPUT == "ALL":
            for repo in SATELLITE_REPOS:
                dispatch_cross_repo_signal(repo)
        else:
            dispatch_cross_repo_signal(TARGET_INPUT)
    else:
        print("\nℹ️ Không có danh sách kho vệ tinh ngoại vi. Hoàn tất tác vụ nội bộ.")

    print("\n✅ Hoàn tất tiến trình vận hành ESEB Rotator!")

if __name__ == "__main__":
    main()
