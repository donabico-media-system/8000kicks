import os
import json
import sys
import time
import requests

CLASSIC_TOKEN = os.getenv("ESEB_CLASSIC_TOKEN")
ORG_NAME = os.getenv("PRIMARY_ORG", "donabico-media-system")
TARGET_INPUT = os.getenv("TARGET_REPO_INPUT", "ALL")
CURRENT_REPO = os.getenv("GITHUB_REPOSITORY", "").split("/")[-1]

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

def auto_discover_all_repositories():
    """Tác vụ 2: Tự động quét toàn bộ kho trong Organization qua GitHub API."""
    print(f"🔍 [AUTO-DISCOVERY] Đang quét toàn bộ các kho thuộc Organization: '{ORG_NAME}'...")
    headers = {
        "Authorization": f"Bearer {CLASSIC_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    discovered_repos = []
    page = 1
    per_page = 100  # Tối đa 100 repo mỗi trang API

    while True:
        # Gọi API lấy danh sách kho của Organization (hỗ trợ phân trang cho hàng ngàn kho)
        url = f"https://api.github.com/orgs/{ORG_NAME}/repos?per_page={per_page}&page={page}&type=all"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            
            # Nếu ORG_NAME là User Account cá nhân thay vì Organization, chuyển sang API User
            if res.status_code == 404 and page == 1:
                url = f"https://api.github.com/user/repos?per_page={per_page}&page={page}&affiliation=owner"
                res = requests.get(url, headers=headers, timeout=10)

            if res.status_code != 200:
                print(f"⚠️ Không thể quét danh sách kho (HTTP {res.status_code}): {res.text}")
                break

            data = res.json()
            if not data:
                break

            for repo_info in data:
                repo_name = repo_info.get("name")
                # Lọc bỏ kho hiện tại để tránh tự lặp tiến trình
                if repo_name and repo_name != CURRENT_REPO:
                    discovered_repos.append(repo_name)

            if len(data) < per_page:
                break
            page += 1

        except Exception as e:
            print(f"❌ Lỗi khi tự động dò tìm kho: {str(e)}")
            break

    print(f"🎯 [AUTO-DISCOVERY] Tự động phát hiện {len(discovered_repos)} kho vệ tinh trong hệ thống.")
    return discovered_repos

def dispatch_cross_repo_signal(target_repo):
    """Tác vụ 3: Bắn tín hiệu kích hoạt tới kho chỉ định."""
    url = f"https://api.github.com/repos/{ORG_NAME}/{target_repo}/dispatches"
    headers = {
        "Authorization": f"Bearer {CLASSIC_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    payload = {
        "event_type": "FORCE_ESEB_ROTATE",
        "client_payload": {
            "source": CURRENT_REPO,
            "anchor": "¢24",
            "timestamp": int(time.time())
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 204:
            print(f"🚀 [CASCADE DISPATCH] Bắn tín hiệu thành công tới kho: {target_repo}")
        elif response.status_code == 404:
            print(f"⏭️ Bỏ qua kho '{target_repo}' (Chưa cấu hình repository_dispatch hoặc thiếu quyền).")
        else:
            print(f"⚠️ Kho {target_repo} trả về HTTP {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Lỗi kết nối API tới kho {target_repo}: {str(e)}")

def main():
    if not CLASSIC_TOKEN:
        print("❌ LỖI BẢO MẬT: Chưa khai báo ESEB_CLASSIC_TOKEN trong Secrets!")
        sys.exit(1)

    print("=== KÍCH HOẠT HỆ THỐNG ESEB DYNAMIC HYPER (AUTO-DISCOVERY 100%) ===")
    
    # 1. Cập nhật state nội bộ
    update_internal_eseb_state()

    # 2. Điều hướng bắn tín hiệu
    if TARGET_INPUT != "ALL":
        print(f"\n🎯 Chế độ chọn lọc: Chỉ phát sóng tới kho chỉ định '{TARGET_INPUT}'")
        dispatch_cross_repo_signal(TARGET_INPUT)
    else:
        # Tự động quét 100% toàn bộ kho trong hệ thống
        target_repos = auto_discover_all_repositories()
        if target_repos:
            print("\n📡 [CASCADE BROADCAST] Đang phát sóng điều khiển tới tất cả các kho...")
            for repo in target_repos:
                dispatch_cross_repo_signal(repo)
        else:
            print("\nℹ️ Không tìm thấy kho vệ tinh nào khác trong hệ thống.")

    print("\n✅ Hoàn tất tiến trình vận hành ESEB Rotator Auto-Discovery!")

if __name__ == "__main__":
    main()
