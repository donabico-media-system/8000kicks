#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Google-Siphon.py (Async Architecture)"""

import argparse
import asyncio
import httpx
from typing import Dict, List, Optional
from pydantic import BaseModel

GOOGLE_BOTS = [
    {"name": "AdsBot_Google", "ua": "AdsBot-Google (+http://www.google.com/adsbot.html)"},
    {"name": "Googlebot_Desktop", "ua": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"},
    {"name": "Google_Extended_AI", "ua": "Mozilla/5.0 (compatible; Google-Extended)"},
    {"name": "Googlebot_Mobile", "ua": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MTC26L) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"},
    {"name": "AdsBot_Google_Mobile", "ua": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AdsBot-Google-Mobile (+http://www.google.com/adsbot.html)"},
    {"name": "Mediapartners_AdSense", "ua": "Mediapartners-Google"},
    {"name": "Google_Adwords_Instant", "ua": "Google-Adwords-Instant (+http://www.google.com/adsbot.html)"},
    {"name": "Google_User_Ad_Clicks", "ua": "Google-User-Ad-Clicks"},
    {"name": "Google_DisplayAds", "ua": "Google-Display-Ads"}
]

class GoogleBotResult(BaseModel):
    bot: str
    status: Optional[int] = None
    error: Optional[str] = None

class GoogleEngine:
    async def siphon_google(self, client: httpx.AsyncClient, url: str, bot: Dict) -> GoogleBotResult:
        try:
            resp = await client.get(url, headers={"User-Agent": bot["ua"]}, timeout=15.0)
            return GoogleBotResult(bot=bot["name"], status=resp.status_code)
        except Exception as e:
            return GoogleBotResult(bot=bot["name"], error=str(e)[:50])

    async def run(self, url: str) -> List[GoogleBotResult]:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            tasks = [self.siphon_google(client, url, bot) for bot in GOOGLE_BOTS]
            return await asyncio.gather(*tasks)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True)
    args = parser.parse_args()
    
    print(f"[V3000-Ω] Google-Siphon | Target: {args.url}")
    results = asyncio.run(GoogleEngine().run(args.url))
    for res in results:
        icon = "✅" if res.status == 200 else "❌"
        print(f"  {icon} [{res.bot}] status={res.status}")

if __name__ == "__main__":
    main()
