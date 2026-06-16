#!/usr/bin/env python3
"""
Bing-Siphon.py (GitHub Optimized v2)
"""

import argparse
import concurrent.futures
import random
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Dict

MICROSOFT_BOTS = [
    {"name": "BingBot_Standard", "ua": "Mozilla/5.0 (compatible; bingbot/2.0)"},
    {"name": "BingPreview_Mobile", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 BingPreview/1.0b"},
    {"name": "MSN_AdBot", "ua": "MSNBot-Media/1.1"},
    {"name": "Microsoft_Copilot", "ua": "Mozilla/5.0 (compatible; Microsoft-Copilot/1.0)"},
]

def get_headers(bot: Dict) -> Dict:
    return {"User-Agent": bot["ua"], "Accept": "text/html,application/xhtml+xml"}

def siphon_with_retry(target_url: str, bot: Dict, max_retries: int = 3) -> Dict:
    result = {"bot": bot["name"], "timestamp": datetime.now(timezone.utc).isoformat(), "status": None, "error": None}
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(target_url, headers=get_headers(bot))
            with urllib.request.urlopen(req, timeout=25) as resp:
                result["status"] = resp.status
                return result
        except Exception as e:
            result["error"] = str(e)[:100]
            if attempt < max_retries:
                time.sleep(random.uniform(4, 8) * attempt)
    return result

def ping_bing_sitemap(target_url: str) -> Dict:
    result = {"action": "bing_sitemap_ping", "status": None, "error": None}
    try:
        ping_url = f"https://www.bing.com/ping?sitemap={urllib.parse.quote(target_url)}"
        req = urllib.request.Request(ping_url, headers={"User-Agent": "DONABICO-V3000"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            result["status"] = resp.status
    except Exception as e:
        result["error"] = str(e)[:80]
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, default="https://donabico-global-media.github.io/8000kicks/")
    parser.add_argument("--concurrent", type=int, default=2)
    args = parser.parse_args()

    print(f"[V3000-Ω] Bing-Siphon (GitHub Mode)")

    # Sitemap Ping
    ping = ping_bing_sitemap(args.url)
    icon = "✅" if ping["status"] == 200 else "⚠️"
    print(f"  {icon} [Bing Sitemap Ping] status={ping['status']}")

    # Bot blasting
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrent) as executor:
        futures = {executor.submit(siphon_with_retry, args.url, bot): bot for bot in MICROSOFT_BOTS}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            results.append(res)
            icon = "✅" if res["status"] == 200 else "❌"
            print(f"  {icon} [{res['bot']}] status={res['status']}")
            time.sleep(random.uniform(3, 6))

    success = sum(1 for r in results if r["status"] == 200)
    print(f"[REPORT] Success: {success}/{len(results)}")

if __name__ == "__main__":
    main()
