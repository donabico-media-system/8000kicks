import os
from bs4 import BeautifulSoup

def run():
    print("[+] ADTech-Traffic: Đang thiết lập hạ tầng phân tích luồng Paid Traffic...")
    file_path = "index.html"
    
    if not os.path.exists(file_path):
        print("[-] Không tìm thấy file index.html để cấu hình.")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # 1. NHÚNG BỘ THEO DÕI NGUỒN TRAFFIC REAL-TIME (UTM MONITOR)
    traffic_script_id = "dnbc-paid-traffic-monitor"
    existing_script = soup.find("script", id=traffic_script_id)
    if existing_script: 
        existing_script.decompose() # Xóa bản cũ nếu có để ghi đè bản mới sạch sẽ

    traffic_script_tag = soup.new_tag("script", id=traffic_script_id)
    traffic_script_tag.string = """
        function parseAdTechTraffic() {
            try {
                const urlParams = new URLSearchParams(window.location.search);
                const source = urlParams.get('utm_source');
                
                if (source) {
                    console.log(`[ADTech Active] Ghi nhận luồng Traffic Thực địa từ nguồn: ${source.toUpperCase()}`);
                    
                    // Lưu nguồn traffic vào Session để giữ vết chân người dùng khi họ lướt trang
                    sessionStorage.setItem('dnbc_traffic_source', source);
                    
                    // Tùy biến: Nếu là traffic từ MGID, ta có thể đánh dấu ưu tiên xử lý ROI
                    if (source === 'mgid') {
                        document.body.setAttribute('data-traffic-tier', 'high-ticket');
                    }
                }
            } catch (e) {
                console.log("[-] Traffic monitor internal error.");
            }
        }
        window.addEventListener('DOMContentLoaded', parseAdTechTraffic);
    """
    
    if soup.head: 
        soup.head.append(traffic_script_tag)
    else: 
        soup.append(traffic_script_tag)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
        
    print("[===] ADTech-Traffic: Cổng phân tích dữ liệu MGID đã online và nhúng vào index.html thành công.")

if __name__ == "__main__":
    run()
