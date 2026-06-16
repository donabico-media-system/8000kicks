#!/usr/bin/env python3
"""
Bing-Siphon.py
EATHESEN V3000-Ω | Microsoft Bing Siphon Module | Indexing Acceleration Layer
Kho 8000Kicks — Fast Bing/Copilot indexing for high-converting landing pages
Features: Sitemap ping + Concurrent Microsoft bot blasting + Stealth jitter
V-STAMP 24 AUTHENTICATED | ¢24 IMMUTABLE | BIÊN HÒA 2026
"""

import argparse
import concurrent.futures
import json
import random
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Dict, List

# ==================== 2026 MICROSOFT CRAWLER MATRIX ====================
MICROSOFT_BOTS = [
    {"name": "BingBot_Standard",      "ua": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"},
    {"name": "BingPreview_Mobile",    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 BingPreview/1.0b"},
    {"name": "MSN_AdBot",             "ua": "MSNBot-Media/1.1 (+http://search.msn.com/msnbot.htm)"},
    {"name": "BingBot_Mobile",        "ua": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 BingBot/2.0"},
    {"name": "Microsoft_Copilot",     "ua": "Mozilla/5.0 (compatible; Microsoft-Copilot/1.0; +https://www.bing.com/copilot)"},
    {"name": "Bing_AdCenter",         "ua": "Mozilla/5.0 (compatible; adidxbot/2.0; +http://www.bing.com/bingbot.htm)"},
    {"name": "MSNBot_News",           "ua": "msnbot-News/1.1 (+http://search.msn.com/msnbot.htm)"},
    {"name": "Bingbot_DeepCrawl",     "ua": "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm) DeepCrawl"},
]

def get_headers(bot: Dict) -> Dict:
    return {
        "User-Agent": bot["ua"],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "X-Siphon-Source": "DONABICO-GLOBAL-MEDIA-V3000",
        "X-EATHESEN-Bing-Siphon": "Neural-V3000-Ω",
        "X-V-STAMP": "24",
    }

def ping_bing_sitemap(target_url: str) -> Dict:
    """Ping Bing sitemap for faster indexing"""
    start = time.time()
    result = {
        "action": "bing_sitemap_ping",
        "url": target_url,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": None,
        "latency_ms": None,
        "error": None,
    }
    try:
        ping_url = f"https://www.bing.com/ping?sitemap={urllib.parse.quote(target_url)}"
        req = urllib.request.Request(ping_url, headers={"User-Agent": "DONABICO-ENGINE-V3000-Ω"})
        with urllib.request.urlopen(req, timeout=15) as response:
            result["status"] = response.status
            result["latency_ms"] = round((time.time() - start) * 1000, 1)
    except Exception as e:
        result["error"] = str(e)[:120]
        result["latency_ms"] = round((time.time() - start) * 1000, 1)
    return result

def siphon_microsoft_bot(target_url: str, bot: Dict) -> Dict:
    start = time.time()
    result = {
        "bot": bot["name"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "url": target_url,
        "status": None,
        "latency_ms": None,
        "error": None,
    }
    try:
        req = urllib.request.Request(target_url, headers=get_headers(bot))
        with urllib.request.urlopen(req, timeout=18) as response:
            result["status"] = response.status
            result["latency_ms"] = round((time.time() - start) * 1000, 1)
    except Exception as e:
        result["error"] = str(e)[:120]
        result["latency_ms"] = round((time.time() - start) * 1000, 1)
    return result

def main():
    parser = argparse.ArgumentParser(
        description="EATHESEN V3000-Ω Bing-Siphon — Microsoft Bing/Copilot Indexing Accelerator for 8000Kicks"
    )
    parser.add_argument("--url", type=str, help="Target URL or sitemap URL")
    parser.add_argument("--urls-file", type=str, help="File with one URL per line")
    parser.add_argument("--concurrent", type=int, default=4, help="Max concurrent bot threads (default: 4)")
    parser.add_argument("--jitter-min", type=float, default=1.2)
    parser.add_argument("--jitter-max", type=float, default=2.8)
    parser.add_argument("--skip-ping", action="store_true", help="Skip Bing sitemap ping")
    parser.add_argument("--output-json", type=str, help="Save results to JSON file")
    args = parser.parse_args()

    urls: List[str] = []
    if args.url:
        urls.append(args.url.strip())
    if args.urls_file:
        with open(args.urls_file, "r", encoding="utf-8") as f:
            urls.extend([line.strip() for line in f if line.strip()])

    if not urls:
        urls = ["https://donabico-global-media.github.io/8000kicks/"]

    print(f"[V3000-Ω] Bing-Siphon started | Targets: {len(urls)} | Bots: {len(MICROSOFT_BOTS)} | Concurrency: {args.concurrent}")

    all_results: List[Dict] = []

    for url in urls:
        print(f"\n[MICROSOFT BING] Target → {url}")

        # 1. Sitemap Ping (optional)
        if not args.skip_ping:
            ping_result = ping_bing_sitemap(url)
            all_results.append(ping_result)
            status_icon = "✅" if ping_result["status"] == 200 else "⚠️"
            print(f"  {status_icon} [Bing Sitemap Ping] status={ping_result['status']} | {ping_result['latency_ms']}ms")

        # 2. Concurrent Bot Blasting
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrent) as executor:
            future_to_bot = {executor.submit(siphon_microsoft_bot, url, bot): bot for bot in MICROSOFT_BOTS}
            for future in concurrent.futures.as_completed(future_to_bot):
                res = future.result()
                all_results.append(res)
                status_icon = "✅" if res["status"] and 200 <= res["status"] < 400 else "❌"
                print(f"  {status_icon} [{res['bot']}] status={res['status']} | {res['latency_ms']}ms")
                time.sleep(random.uniform(args.jitter_min, args.jitter_max))

    # Summary
    success = sum(1 for r in all_results if r.get("status") and 200 <= r["status"] < 400)
    rate = (success / len(all_results) * 100) if all_results else 0
    print(f"\n[REPORT] Success: {success}/{len(all_results)} ({rate:.1f}%) | {datetime.now(timezone.utc).isoformat()}")

    if args.output_json:
        payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "v_stamp": "24",
            "core": "EATHESEN_V3000_Ω_Bing-Siphon",
            "hằng_số": "¢24",
            "targets": urls,
            "results": all_results,
        }
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        print(f"[LOG] Results saved → {args.output_json}")

if __name__ == "__main__":
    main()
