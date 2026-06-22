import os
import re
from bs4 import BeautifulSoup

def run():
    print("[+] Performance-Max: Đang quét sâu thanh lọc thông tin ảo...")
    file_path = "index.html"
    if not os.path.exists(file_path): return

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    fake_patterns = [
        r"Only \d+ pairs left.*", 
        r"Chỉ còn \d+ đôi trong kho.*",
        r"Giảm giá \d+% trong \d+ phút.*",
        r"Flash sale.*",
        r"Khuyến mãi trực tiếp tại kho hàng.*"
    ]

    for element in soup.find_all(text=True):
        text_value = element.strip()
        for pattern in fake_patterns:
            if re.search(pattern, text_value, re.IGNORECASE):
                element.replace_with("")
                break

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("[===] Performance-Max: Toàn bộ nội dung đã được làm sạch minh bạch.")

if __name__ == "__main__":
    run()
