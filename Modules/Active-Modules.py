#!/usr/bin/env python3
"""
EATHESEN V3000-Ω | 8000KICKS LIVE FACTORY INJECTOR
Chức năng: Kích hoạt ma trận Siphon kèm tham số và TIÊM TRỰC TIẾP 100% vào Landing Page 8000Kicks
"""
import os
import re
import sys
from datetime import datetime, timezone

def run_all_siphons(target_url):
    print(f"[V3000-8000KICKS] Khởi chạy chuỗi module quan trắc ngầm cho URL: {target_url}")
    
    # GIẢI PHÁP SỬA LỖI: Truyền trực tiếp tham số --url vào các module con để chặn lỗi Argument Error
    os.system(f"python3 Traffic-Siphon.py --url {target_url}")
    os.system(f"python3 Affiliate-Network-Siphon.py --url {target_url}")
    os.system(f"python3 SEO-Shield-Siphon.py --url {target_url}")
    os.system(f"python3 Social-Preview-Siphon.py --url {target_url}")
    os.system(f"python3 Google-Siphon.py --url {target_url}")
    os.system(f"python3 Bing-Siphon.py --url {target_url}")

def inject_production_html(target_url):
    index_path = os.path.join("..", "index.html")
    if not os.path.exists(index_path):
        index_path = "index.html"
        
    if not os.path.exists(index_path):
        print("[ERROR] Không tìm thấy file index.html của 8000Kicks!")
        return

    print(f"[V3000-INJECTOR] Đại phẫu và tiêm dữ liệu vào: {index_path}")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. THỪA HƯỞNG TỪ SEO-SHIELD: Bơm từ khóa giày gai dầu chống nước vào Head
    seo_tags = """
    <meta name="keywords" content="8000Kicks, giày gai dầu, giày chống nước, waterproof hemp shoes, sustainable footwear, Donabico Global Media">
    <meta name="description" content="Khám phá dòng giày làm từ sợi gai dầu tự nhiên chống nước 100% của 8000Kicks tại phân khu Donabico.">"""
    if "<head>" in html and "8000Kicks" not in html:
        html = html.replace("<head>", f"<head>{seo_tags}")

    # 2. THỪA HƯỞNG TỪ SOCIAL-PREVIEW: Tối ưu OpenGraph hiển thị link mạng xã hội
    og_tags = """
    <meta property="og:title" content="8000Kicks - Giày Gai Dầu Chống Nước Đầu Tiên Trên Thế Giới">
    <meta property="og:image" content="https://donabico-global-media.github.io/8000kicks/assets/hemp-shoes-banner.jpg">"""
    if "<head>" in html and "og:title" not in html:
        html = html.replace("<head>", f"<head>{og_tags}")

    # 3. THỪA HƯỞNG TỪ TRAFFIC-SIPHON: Tiêm thanh trạng thái Donabico Global Media System
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    status_banner = f"""
    <div id="dnbc-adtech-banner" style="background: linear-gradient(90deg, #11998e, #38ef7d); color: #000; text-align: center; font-family: sans-serif; font-size: 11px; padding: 6px; font-weight: bold; border-bottom: 2px solid #fff;">
        🛡️ DONABICO GLOBAL MEDIA SYSTEM | 8000KICKS NODE ACTIVE AT {current_time}
    </div>"""
    html = re.sub(r'<div id="dnbc-adtech-banner">.*?</div>', '', html, flags=re.DOTALL)
    if "<body>" in html:
        html = html.replace("<body>", f"<body>\n    {status_banner}")

    # 4. THỪA HƯỞNG TỪ AFFILIATE-NETWORK: Cố định tuyến link phân phối tiếp thị liên kết trực tiếp
    target_aff_url = "https://donabico-global-media.github.io/shop/8000kicks.html"
    html = re.sub(r'href="[^"]*placeholder_affiliate_link[^"]*"', f'href="{target_aff_url}"', html)

    # 5. THỪA HƯỞNG TỪ AI-CACHE-SIPHON: Nén dung lượng HTML cực hạn
    compressed_html = "\n".join([line.strip() for line in html.split("\n") if line.strip()])

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(compressed_html)
    print("[SUCCESS] Lộ trình tiêm dữ liệu trực tiếp 100% vào 8000Kicks hoàn tất!")

if __name__ == "__main__":
    # Đọc tham số URL truyền từ file Workflow, mặc định nếu không truyền là link 8000kicks
    target = "https://donabico-global-media.github.io/8000kicks/"
    if "--url" in sys.argv:
        idx = sys.argv.index("--url")
        if idx + 1 < len(sys.argv):
            target = sys.argv[idx + 1]

    run_all_siphons(target)
    inject_production_html(target)
