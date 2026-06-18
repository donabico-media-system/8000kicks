#!/usr/bin/env python3
"""
EATHESEN V3000-Ω | ULTRA MULTI-THREADING INJECTOR WITH GREEN VISUAL SHIELD (8000KICKS)
Chức năng: Tự động phát hiện HÀNG NGÀN module, chạy SONG SONG siêu tốc và TIÊM KHUNG VIỀN XANH LÁ 2PX
Bản vá: Sửa lỗi lặp thanh trạng thái (Dọn sạch banner cũ trước khi tiêm banner mới)
"""
import os
import re
import sys
import concurrent.futures
from datetime import datetime, timezone

def execute_single_module(module_file, target_url):
    """Hàm thực thi một module độc lập và bắt lỗi tránh làm sập luồng chính"""
    if module_file == "Active-Modules.py":
        return None
        
    try:
        # Ép chạy kèm tham số --url khép kín để chặn lỗi Argument Error
        exit_code = os.system(f"python3 {module_file} --url {target_url} > /dev/null 2>&1")
        if exit_code == 0:
            return f"✅ {module_file} -> Success"
        else:
            return f"❌ {module_file} -> Failed (Code {exit_code})"
    except Exception as e:
        return f"💥 {module_file} -> Error: {str(e)}"

def run_massive_siphon_matrix(target_url):
    print("[V3000-Ω] Khởi chạy bộ quét tự động cấu trúc đa luồng...")
    all_files = os.listdir(".")
    module_targets = [f for f in all_files if f.endswith(".py") and f != "Active-Modules.py"]
    
    print(f"[V3000-Ω] Phát hiện tổng cộng {len(module_targets)} module thực chiến.")
    
    results = []
    max_workers = 50 
    
    print(f"[V3000-Ω] Đang phân bổ ma trận vào {max_workers} luồng xử lý cao tốc...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(execute_single_module, mod, target_url): mod for mod in module_targets}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                results.append(res)
                
    print(f"[V3000-Ω] Hoàn thành quét ma trận. Đã xử lý {len(results)}/{len(module_targets)} module.")

def inject_production_html():
    index_path = os.path.join("..", "index.html")
    if not os.path.exists(index_path): index_path = "index.html"
    if not os.path.exists(index_path): return

    print(f"[V3000-INJECTOR] Tiến hành đại phẫu toàn diện và tiêm Khung viền Xanh lá...")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. TIÊM KHUNG VIỀN XANH LÁ (GREEN) 2PX: Chèn CSS viền xanh lá vào <head> nếu chưa có
    green_border_css = "<style>body { border: 2px solid green !important; box-sizing: border-box; }</style>"
    if "<head>" in html and "border: 2px solid green" not in html:
        html = html.replace("<head>", f"<head>{green_border_css}")

    # 2. SEO-SHIELD: Bơm từ khóa giày gai dầu chống nước vào Head
    seo_tags = """
    <meta name="keywords" content="8000Kicks, giày gai dầu, giày chống nước, waterproof hemp shoes, sustainable footwear, Donabico Global Media">
    <meta name="description" content="Khám phá dòng giày làm từ sợi gai dầu tự nhiên chống nước 100% của 8000Kicks tại phân khu Donabico.">"""
    if "<head>" in html and "8000Kicks" not in html:
        html = html.replace("<head>", f"<head>{seo_tags}")

    # 3. SOCIAL-PREVIEW: Tối ưu OpenGraph hiển thị khi share link mạng xã hội
    og_tags = """
    <meta property="og:title" content="8000Kicks - Giày Gai Dầu Chống Nước Đầu Tiên Trên Thế Giới">
    <meta property="og:image" content="https://donabico-global-media.github.io/8000kicks/assets/hemp-shoes-banner.jpg">"""
    if "<head>" in html and "og:title" not in html:
        html = html.replace("<head>", f"<head>{og_tags}")

    # 4. GIẢI PHÁP DIỆT TẬN GỐC LỖI LẶP BANNER: 
    # Quét sạch tất cả các tag banner cũ (kể cả dạng xuống dòng hay dạng viết liền một dòng do nén code)
    html = re.sub(r'<div id="dnbc-adtech-banner".*?</div>', '', html, flags=re.DOTALL)

    # Khởi tạo banner mới với mốc thời gian UTC hiện tại
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    status_banner = f'<div id="dnbc-adtech-banner" style="background: linear-gradient(90deg, #11998e, #38ef7d); color: #000; text-align: center; font-family: sans-serif; font-size: 11px; padding: 6px; font-weight: bold; border-bottom: 2px solid #fff;">🛡️ DONABICO GLOBAL MEDIA SYSTEM | MASSIVE MATRIX NODE ACTIVE AT {current_time}</div>'
    
    if "<body>" in html:
        html = html.replace("<body>", f"<body>{status_banner}")

    # 5. AFFILIATE-NETWORK: Tuyến link phân phối tiếp thị liên kết trực tiếp
    target_aff_url = "https://donabico-global-media.github.io/shop/8000kicks.html"
    html = re.sub(r'href="[^"]*placeholder_affiliate_link[^"]*"', f'href="{target_aff_url}"', html)

    # 6. Nén mã nguồn cực hạn loại bỏ khoảng trắng thừa
    compressed_html = "\n".join([line.strip() for line in html.split("\n") if line.strip()])

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(compressed_html)
    print("[SUCCESS] Bản vá hoàn tất! Đã dọn sạch thanh banner cũ và tối ưu hóa 8000Kicks!")

if __name__ == "__main__":
    target = "https://donabico-global-media.github.io/8000kicks/"
    if "--url" in sys.argv:
        idx = sys.argv.index("--url")
        if idx + 1 < len(sys.argv): target = sys.argv[idx + 1]

    run_massive_siphon_matrix(target)
    inject_production_html()
