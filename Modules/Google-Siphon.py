#!/usr/bin/env python3
"""
Google-Siphon.py (GitHub Optimized v3.5 - Google Display Network Integrated)
EATHESEN V3000-Ω | Google Matrix Optimization
"""

import argparse
import concurrent.futures
import random
import time
import urllib.parse
import urllib.request
import urllib.error
from typing import Dict

# 🎯 MA TRẬN BOT GOOGLE TOÀN DIỆN (ĐÃ TÍCH HỢP HỆ THỐNG HIỂN THỊ DISPLAY VÀ ADSENSE)
GOOGLE_BOTS = [
    {"name": "Googlebot_Desktop", "ua": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"},
    {"name": "Googlebot_Mobile", "ua": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MTC26L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"},
    {"name": "Google_Extended_AI", "ua": "Mozilla/5.0 (compatible; Google-Extended)"},
    {"name": "AdsBot_Google", "ua": "AdsBot-Google (+http://www.google.com/adsbot.html)"},
    {"name": "AdsBot_Google_Mobile", "ua": "Mozilla/5.0 (Linux; Android 5.0; SM-G920A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 AdsBot-Google-Mobile"},
    # 🌟 PHÂN HỆ GOOGLE DISPLAY NETWORK & ADSENSE BỔ SUNG:
    {"name": "Mediapartners_AdSense", "ua": "Mediapartners-Google"},
    {"name": "Google_Adwords_Instant", "ua": "AdWords-KeywordsMedicalId-Samplest (+http://www.google.com/adsbot.html)"},
    {"name": "Google_User_Ad_Clicks", "ua": "Mozilla/5.0 (compatible; Google-Adwords-User-Clicks; +http://www.google.com/adsbot.html)"},
    {"name": "Google_DisplayAds", "ua": "Mozilla/5.0 (compatible; Google-Display-Ads-Bot)"}
]

def get_headers(bot: Dict) -> Dict:
    return {
        "User-Agent": bot["ua"], 
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "X-AdTech-Gateway": "Donabico-REST-Gateway" # Giữ định danh kết nối đồng bộ
    }

def siphon_with_retry(target_url: str, bot: Dict, max_retries: int = 3) -> Dict:
    result = {"bot": bot["name"], "status": None, "error": None}
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(target_url, headers=get_headers(bot))
            with urllib.request.urlopen(req, timeout=25) as resp:
                result["status"] = resp.status
                return result
        except urllib.error.HTTPError as e:
            result["status"] = e.code
            if e.code in (404, 403): 
                break
            time.sleep(random.uniform(2, 4) * attempt)
        except Exception as e:
            result["error"] = str(e)[:80]
            if attempt < max_retries: 
                time.sleep(random.uniform(2, 4) * attempt)
    return result

def ping_google_sitemap(target_url: str) -> Dict:
    result = {"status": None}
    try:
        ping_url = f"https://www.google.com/ping?sitemap={urllib.parse.quote(target_url)}"
        req = urllib.request.Request(ping_url, headers={"User-Agent": "DONABICO-V3000"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            result["status"] = resp.status
    except urllib.error.HTTPError as e:
        result["status"] = e.code
    except Exception:
        pass
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True)
    args = parser.parse_args()

    print(f"[V3000-Ω] Google-Siphon | Target: {args.url}")
    
    # Thực hiện Ping kiểm tra sơ đồ trang web
    ping = ping_google_sitemap(args.url)
    sitemap_icon = "✅" if ping["status"] == 200 else "⚠️"
    print(f"  {sitemap_icon} [Google Sitemap Ping] status={ping['status']}")

    # Đồng loạt tung các luồng bot càn quét
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(siphon_with_retry, args.url, bot): bot for bot in GOOGLE_BOTS}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            icon = "✅" if res["status"] == 200 else "❌"
            print(f"  {icon} [{res['bot']}] status={res['status']}")
            time.sleep(random.uniform(0.5, 1.5))

if __name__ == "__main__":
    main()
