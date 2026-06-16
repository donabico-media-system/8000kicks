#!/usr/bin/env python3
"""Google-Siphon.py (GitHub Optimized v3 - Flawless Mode)"""

import argparse
import concurrent.futures
import random
import time
import urllib.parse
import urllib.request
import urllib.error
from typing import Dict

GOOGLE_BOTS = [
    {"name": "Googlebot_Desktop", "ua": "Mozilla/5.0 (compatible; Googlebot/2.1)"},
    {"name": "Googlebot_Mobile", "ua": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Googlebot/2.1"},
    {"name": "AdsBot_Google", "ua": "AdsBot-Google"},
]

def get_headers(bot: Dict) -> Dict:
    return {"User-Agent": bot["ua"], "Accept": "text/html,application/xhtml+xml"}

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
            if e.code in (404, 403): break
            time.sleep(random.uniform(2, 4) * attempt)
        except Exception as e:
            result["error"] = str(e)[:80]
            if attempt < max_retries: time.sleep(random.uniform(2, 4) * attempt)
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
    ping = ping_google_sitemap(args.url)
    print(f"  {'✅' if ping['status'] == 200 else '⚠️'} [Google Sitemap Ping] status={ping['status']}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(siphon_with_retry, args.url, bot): bot for bot in GOOGLE_BOTS}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            icon = "✅" if res["status"] == 200 else "❌"
            print(f"  {icon} [{res['bot']}] status={res['status']}")
            time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    main()
