#!/usr/bin/env python3
"""
EATHESEN V3000-Ω | AUTONOMOUS MATRIX INJECTOR (GREEN VISUAL SHIELD 2PX)
Bản vá: Sửa triệt để lỗi Argument --url của module con, dọn sạch banner cũ và tiêm viền xanh.
"""
import os
import re
import sys
import concurrent.futures
from datetime import datetime, timezone

def execute_single_module(module_file, target_url):
    """Hàm thực thi module độc lập, truyền tham số chuẩn xác định dạng để chặn lỗi Argument"""
    if module_file == "Active-Modules.py":
        return None
        
    try:
        # Sử dụng sys.executable để gọi đúng môi trường python và bọc URL trong dấu nháy đơn bảo mật
        cmd = f"'{sys.executable}' '{module_file}' --url '{target_url}' > /dev/null 2>&1"
        exit_code = os.system(cmd)
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
                
    print("[V3000-Ω] Hoàn thành quét ma trận module con.")

def inject_production_html():
    # Định vị file index.html nằm ở thư mục cha
    index_path = os.path.join("..", "index.html")
    if not os.path.exists(index_path): index_path = "index.html"
    if not os.path.exists(index_path): 
        print("[ERROR] Không tìm thấy file index.html!")
        return

    print(f"[V3000-INJECTOR] Tiến hành đại phẫu toàn diện và tiêm Khung viền Xanh lá...")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. TIÊM KHUNG VIỀN XANH LÁ (GREEN) 2PX VÀO THẺ BODY (Ép hiển thị đè đè lên viền đỏ)
    green_style = "border: 2px solid green !important; box-sizing: border-box; min-height: 100vh;"
    if "body {" in html:
        # Nếu trong file đã có đoạn định nghĩa style cho body, tiêm đè thuộc tính vào
        html = re.sub(r'body\s*{([^}]*)}', f'body {{\g<1> border: 2px solid green !important; box-sizing: border-box;}}', html)
    else:
        # Nếu chưa có style, chèn đoạn style riêng vào đầu thẻ <head>
        green_border_css = "<style>body { border: 2px solid green !important; box-sizing: border-box; }</style>"
        if "<head>" in html:
            html = html.replace("<head>", f"<head>\n{green_border_css}")

    # 2. SEO-SHIELD & SOCIAL PREVIEW
    seo_tags = """
    <meta name="keywords" content="8000Kicks, giày gai dầu, giày chống nước, waterproof hemp shoes, sustainable footwear, Donabico Global Media">
    <meta name="description" content="Khám phá dòng giày làm từ sợi gai dầu tự nhiên chống nước 100% của 8000Kicks tại phân khu Donabico.">"""
    if "<head>" in html and "8000Kicks" not in html:
        html = html.replace("<head>", f"<head>{seo_tags}")

    # 3. DỌN SẠCH BANNER CŨ (Xóa toàn bộ các khối banner cũ để tránh lặp)
    html = re.sub(r'<div id="dnbc-adtech-banner".*?</div>', '', html, flags=re.DOTALL)

    # 4. TIÊM DUY NHẤT 1 BANNER MỚI VỚI MÀU NEON XANH LÁ
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    status_banner = f'<div id="dnbc-adtech-banner" style="background: linear-gradient(90deg, #11998e, #38ef7d); color: #000; text-align: center; font-family: sans-serif; font-size: 11px; padding: 6px; font-weight: bold; border-bottom: 2px solid #fff; width: 100%; box-sizing: border-box;">🛡️ DONABICO GLOBAL MEDIA SYSTEM | MASSIVE MATRIX NODE ACTIVE AT {current_time}</div>'
    
    if "<body>" in html:
        html = html.replace("<body>", f"<body>\n    {status_banner}")

    # 5. AFFILIATE LINK MAPPING
    target_aff_url = "https://donabico-global-media.github.io/shop/8000kicks.html"
    html = re.sub(r'href="[^"]*placeholder_affiliate_link[^"]*"', f'href="{target_aff_url}"', html)

    # 6. Nén mã nguồn loại bỏ dòng trống thừa
    compressed_html = "\n".join([line.strip() for line in html.split("\n") if line.strip()])

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(compressed_html)
    print("[SUCCESS] Đã vá lỗi đối số! Tiêm khung viền xanh lá 2px và tối ưu Drone Landing Page hoàn tất!")

if __name__ == "__main__":
    target = "https://donabico-global-media.github.io/8000kicks/"
    if "--url" in sys.argv:
        idx = sys.argv.index("--url")
        if idx + 1 < len(sys.argv): target = sys.argv[idx + 1]

    run_massive_siphon_matrix(target)
    inject_production_html()
