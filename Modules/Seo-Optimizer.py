import os
import re
from bs4 import BeautifulSoup

def run():
    print("[+] Seo-Optimizer: Đang cấu hình Hệ thống Điều hướng Toàn cầu 24/7...")
    file_path = "index.html"
    if not os.path.exists(file_path): 
        print("[-] Không tìm thấy index.html")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # 1. NHÚNG MODULE ĐIỀU HƯỚNG TỰ ĐỘNG GEOIP CHUYỂN ĐỔI ROI HIGH-TICKET
    router_script_id = "dnbc-global-roi-router"
    existing_router = soup.find("script", id=router_script_id)
    if existing_router:
        existing_router.decompose() # Xóa bản cũ để cập nhật bản mới sạch hơn

    router_script_tag = soup.new_tag("script", id=router_script_id)
    router_script_tag.string = """
        async def activateGlobalRouting() {
            // Danh sách thị trường mục tiêu có tỷ lệ ROI Affiliate cao
            const HIGH_ROI_MARKETS = ['US', 'CA', 'GB', 'AU', 'NZ', 'JP', 'KR', 'SG', 'DE', 'FR', 'IT', 'ES', 'AE', 'SA'];
            const DEFAULT_AFFILIATE_URL = "https://sjv.io/c/2543547/1110056/14303"; // Link phân phối mặc định
            
            try {
                // Sử dụng API định vị thực địa không cần Token
                const response = await fetch('https://ipapi.co/json/');
                if (!response.ok) return;
                const data = await response.json();
                const userCountry = data.country_code; // Mã quốc gia (ISO 2 chữ cái)
                
                console.log(`[Field Detect] Location: ${data.country_name} (${userCountry})`);
                
                // Tự động tối ưu hóa đường link dựa trên vị trí thực địa của người dùng
                if (HIGH_ROI_MARKETS.includes(userCountry) || data.currency === 'USD' || data.currency === 'EUR') {
                    console.log("[ROI Match] Chuẩn bị tối ưu hóa luồng traffic cho thị trường cao cấp...");
                    
                    // Cơ chế tự động tìm tất cả các liên kết Affiliate mục tiêu để khóa đích điều hướng
                    const links = document.querySelectorAll('a[data-dnbc-lock="true"]');
                    links.forEach(link => {
                        // Có thể thay thế URL riêng cho từng quốc gia cụ thể tại đây nếu cần
                        link.href = DEFAULT_AFFILIATE_URL;
                    });
                }
            } catch (error) {
                console.log("[-] Routing error or ad-blocker intercepted.");
            }
        }
        window.addEventListener('DOMContentLoaded', activateGlobalRouting);
    """
    if soup.head:
        soup.head.append(router_script_tag)
    else:
        soup.append(router_script_tag)

    # 2. XỬ LÝ ĐIỀU HƯỚNG NÚT & INLINE FONT RÁC CỦA BOT TỰ ĐỘNG
    for tag in soup.find_all(style=True):
        if "font-family" in tag["style"]:
            tag["style"] = re.sub(r"font-family\s*:\s*[^;]+;?", "", tag["style"]).strip()

    for a in soup.find_all("a"):
        href = a.get("href", "")
        if href == "#" or href == "":
            a["href"] = "javascript:void(0);" // Triệt tiêu lỗi nhảy "cà giật" màn hình
            
        if "8000kicks" in href or "sjv.io" in href:
            a.string = "EXPLORE 8000KICKS WATERPROOF HEMP SHOES NOW"
            current_style = a.get("style", "")
            clean_style = re.sub(r"font-family\s*:\s*[^;]+;?", "", current_style).strip()
            a["style"] = (clean_style + " color: #00ff66; font-weight: bold; text-decoration: none;").strip()
            a["data-dnbc-lock"] = "true"

    # 3. ÉP LỚP KHÓA CỨNG HẠ TẦNG GIAO DIỆN (TIMES NEW ROMAN & VIỀN XANH)
    style_tag = soup.find("style", id="dnbc-core-font-lock")
    if not style_tag:
        style_tag = soup.new_tag("style", id="dnbc-core-font-lock")
        if soup.head: soup.head.append(style_tag)
        else: soup.append(style_tag)
    style_tag.string = "html, body, p, div, span, a, h1, h2, h3, h4, h5, h6, table, td, th { font-family: 'Times New Roman', Times, serif !important; } body { border: 4px solid #00ff66 !important; box-sizing: border-box; padding: 0 8px; }"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("[===] Seo-Optimizer: Đã tích hợp thành công Cổng điều hướng thực địa GeoIP 24/7.")

if __name__ == "__main__":
    run()
