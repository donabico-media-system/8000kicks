#!/usr/bin/env python3
"""AI-Cache-Siphon.py (GitHub Optimized v3 - Flawless Mode)"""

import argparse
import concurrent.futures
import random
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from typing import Dict

AI_CRAWLERS = [
    {"name": "OpenAI_ChatGPT_Core", "ua": "Mozilla/5.0 (compatible; GPTBot/1.2; +https://openai.com/gptbot)"},
    {"name": "Google_Gemini_Extended", "ua": "Mozilla/5.0 (compatible; Google-Extended)"},
    {"name": "Anthropic_Claude_Bot", "ua": "Mozilla/5.0 (compatible; Anthropic-AI)"},
    {"name": "Perplexity_AI_Search", "ua": "Mozilla/5.0 (compatible; PerplexityBot/1.0)"},
    {"name": "Microsoft_Copilot", "ua": "Mozilla/5.0 (compatible; bingbot/2.0)"},
    {"name": "xAI_Grok", "ua": "Mozilla/5.0 (compatible; xAI-Grok/1.0)"},
    {"name": "DeepSeek_AI", "ua": "Mozilla/5.0 (compatible; DeepSeekBot/1.0)"},
]

def get_headers(bot: Dict) -> Dict:
    return {
        "User-Agent": bot["ua"],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "X-EATHESEN": "V3000-GitHub",
    }

def siphon_with_retry(target_url: str, bot: Dict, max_retries: int = 3) -> Dict:
    result = {"bot": bot["name"], "status": None, "latency_ms": None, "error": None}
    for attempt in range(1, max_retries + 1):
        start = time.time()
        try:
            req = urllib.request.Request(target_url, headers=get_headers(bot))
            with urllib.request.urlopen(req, timeout=30) as resp:
                result["status"] = resp.status
                result["latency_ms"] = round((time.time() - start) * 1000, 1)
                return result
        except urllib.error.HTTPError as e:
            result["status"] = e.code
            result["latency_ms"] = round((time.time() - start) * 1000, 1)
            result["error"] = str(e)
            if e.code in (404, 403): break # Dừng spam nếu web báo lỗi cấu trúc
            time.sleep(random.uniform(2, 4) * attempt)
        except Exception as e:
            result["error"] = str(e)[:80]
            if attempt < max_retries: time.sleep(random.uniform(2, 4) * attempt)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True)
    args = parser.parse_args()

    print(f"[V3000-Ω] AI-Cache-Siphon | Target: {args.url}")
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(siphon_with_retry, args.url, bot): bot for bot in AI_CRAWLERS}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            results.append(res)
            icon = "✅" if res["status"] == 200 else ("⚠️" if res["status"] else "❌")
            print(f"  {icon} [{res['bot']}] status={res['status']} | {res['latency_ms']}ms")
            time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    main()
