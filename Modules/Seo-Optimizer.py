import os
import re
from bs4 import BeautifulSoup

def run():
    print("[+] Seo-Optimizer: Đang khóa cứng font và thiết lập điều hướng toàn cầu...")
    file_path = "index.html"
    if not os.path.exists(file_path): 
        print("[-] Không tìm thấy index.html để tối ưu.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # 1. NHÚNG MÃ ĐIỀU HƯỚNG TỰ ĐỘNG THEO QUỐC GIA (GEOIP ROI ROUTER)
    router_script_id = "dnbc-global-roi-router"
    existing_router = soup.find("script", id=router_script_id)
    if existing_router:
        existing_router.decompose()

    router_script_tag = soup.new_tag("script", id=router_script_id)
    router_script_tag.string = """
        async function activateGlobalRouting() {
            // Các thị trường trọng điểm có tỷ lệ chuyển đổi ROI Affiliate cao
            const HIGH_ROI_MARKETS = ['US', 'CA', 'GB', 'AU', 'NZ', 'JP', 'KR', 'SG', 'DE', 'FR', 'IT', 'ES', 'AE', 'SA'];
            const DEFAULT_AFFILIATE_URL = "https://sjv.io/c/2543547/1110056/14303";
            
            try {
                // Gọi API thực địa công cộng để nhận biết quốc gia
                const response = await fetch('https://ipapi.co/json/');
                if (!response.ok) return;
                const data = await response.json();
                const userCountry = data.country_code;
                
                console.log(`[GeoIP System] User Location: ${data.country_name} (${userCountry})`);
                
                // Tự động tối ưu hóa đích đến nếu người dùng thuộc nhóm thị trường cao cấp
                if (HIGH_ROI_MARKETS.includes(userCountry) || data.currency === 'USD' || data.currency === 'EUR') {
                    const links = document.querySelectorAll('a[data-dnbc-lock="true"]');
                    links.forEach(link => {
                        link.href = DEFAULT_AFFILIATE_URL;
                    });
                }
            } catch (error) {
                console.log("[-] Routing process bypassed or ad-blocker detected.");
            }
        }
        window.addEventListener('DOMContentLoaded', activateGlobalRouting);
    """
    if soup.head:
        soup.head.append(router_script_tag)
    else:
        soup.append(router_script_tag)

    # 2. THANH LỌC STYLE INLINE VÀ CHUẨN HÓA LIÊN KẾT ĐIỀU HƯỚNG
    for tag in soup.find_all(style=True):
        if "font-family" in tag["style"]:
            tag["style"] = re.sub(r"font-family\s*:\s*[^;]+;?", "", tag["style"]).strip()

    for a in soup.find_all("a"):
        href = a.get("href", "")
        # Thay thế liên kết rỗng để triệt tiêu dứt điểm lỗi màn hình nhảy giật
        if href == "#" or href == "":
            a["href"] = "javascript:void(0);"
            
        # Đồng bộ văn bản hiển thị chuẩn Global cho brand đối tác
        if "8000kicks" in href or "sjv.io" in href:
            a.string = "EXPLORE 8000KICKS WATERPROOF HEMP SHOES NOW"
            current_style = a.get("style", "")
            clean_style = re.sub(r"font-family\s*:\s*[^;]+;?", "", current_style).strip()
            a["style"] = (clean_style + " color: #00ff66; font-weight: bold; text-decoration: none;").strip()
            a["data-dnbc-lock"] = "true"

    # 3. KHÓA CỨNG HẠ TẦNG GIAO DIỆN (FONT TIMES NEW ROMAN & VIỀN XANH HỆ THỐNG)
    style_tag = soup.find("style", id="dnbc-core-font-lock")
    if not style_tag:
        style_tag = soup.new_tag("style", id="dnbc-core-font-lock")
        if soup.head: 
            soup.head.append(style_tag)
        else: 
            soup.append(style_tag)
            
    style_tag.string = "html, body, p, div, span, a, h1, h2, h3, h4, h5, h6, table, td, th { font-family: 'Times New Roman', Times, serif !important; } body { border: 4px solid #00ff66 !important; box-sizing: border-box; padding: 0 8px; }"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("[===] Seo-Optimizer: Đã áp đặt kỷ luật Times New Roman và nhúng cổng GeoIP thành công.")

if __name__ == "__main__":
    run()
