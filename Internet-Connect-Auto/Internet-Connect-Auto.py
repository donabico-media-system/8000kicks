# -*- coding: utf-8 -*-
import requests
from datetime import datetime

class EHCInternetConnectAuto:
    def __init__(self):
        self.log_file = "Connection-Log.txt"
        # Giả lập trình duyệt để vượt qua các bộ lọc Bot/WAF của Wikipedia, Amazon...
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        }
        self.targets = [
            "https://www.google.com", "https://www.cloudflare.com",
            "https://www.github.com", "https://www.bing.com",
            "https://www.wikipedia.org", "https://www.amazon.com",
            "https://www.microsoft.com", "https://www.apple.com",
            "https://www.cloudflare.com/cdn-cgi/trace", "https://www.fast.com",
            "https://www.facebook.com", "https://www.youtube.com",
            "https://www.adobe.com", "https://www.stackoverflow.com"
        ]
        
    def launch_ocean_pulse(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entries = []
        
        for url in self.targets:
            try:
                # Gửi kèm header để trở thành "người dùng" thực sự
                response = requests.get(url, headers=self.headers, timeout=15)
                status = f"SUCCESS({response.status_code})"
            except Exception as e:
                status = f"FAILED"
            
            log_entries.append(f"[{timestamp}] TARGET: {url} -> {status}")
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                for entry in log_entries:
                    f.write(entry + "\n")
            print(f"✅ Đã quét xong {len(self.targets)} đích đến với giả lập trình duyệt.")
        except Exception as e:
            print(f"❌ Lỗi ghi log: {str(e)}")

if __name__ == "__main__":
    EHCInternetConnectAuto().launch_ocean_pulse()
