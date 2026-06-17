#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bing-Siphon.py (Async Mode)"""

import argparse
import asyncio
import random
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
import httpx
from pydantic import BaseModel, Field

MICROSOFT_BOTS = [
    {"name": "BingBot_Standard", "ua": "Mozilla/5.0 (compatible; bingbot/2.0)"},
    {"name": "BingPreview_Mobile", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 BingPreview/1.0b"},
    {"name": "MSN_AdBot", "ua": "MSNBot-Media/1.1"},
]

class BotExecutionResult(BaseModel):
    bot: str
    status: Optional[int] = None
    error: Optional[str] = None
    content_hash: Optional[str] = None

class BingSiphonPayload(BaseModel):
    target_url: str
    execution_latency_ms: float
    bot_responses: List[BotExecutionResult] = []

class BingSiphonEngine:
    async def siphon_with_retry_async(self, client: httpx.AsyncClient, target_url: str, bot: Dict) -> BotExecutionResult:
        headers = {"User-Agent": bot["ua"], "Accept": "text/html,application/xhtml+xml"}
        err_msg, status_code = None, None
        try:
            response = await client.get(target_url, headers=headers, timeout=25.0)
            status_code = response.status_code
        except Exception as e:
            err_msg = str(e)[:50]
        
        v_hash = hashlib.sha256(f"{bot['name']}||{status_code}".encode()).hexdigest()[:10].upper()
        return BotExecutionResult(bot=bot["name"], status=status_code, error=err_msg, content_hash=v_hash)

    async def run(self, target_url: str) -> Dict[str, Any]:
        start_time = asyncio.get_event_loop().time()
        async with httpx.AsyncClient(follow_redirects=True) as client:
            tasks = [self.siphon_with_retry_async(client, target_url, bot) for bot in MICROSOFT_BOTS]
            bot_responses = await asyncio.gather(*tasks)
        end_time = asyncio.get_event_loop().time()
        
        payload = BingSiphonPayload(target_url=target_url, execution_latency_ms=round((end_time - start_time)*1000, 1), bot_responses=list(bot_responses))
        return payload.model_dump()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True)
    args = parser.parse_args()

    print(f"[V3000-Ω] Bing-Siphon (Async Mode) | Target: {args.url}")
    result = asyncio.run(BingSiphonEngine().run(args.url))
    for res in result["bot_responses"]:
        icon = "✅" if res["status"] == 200 else "❌"
        print(f"    {icon} [{res['bot']}] status={res['status']} | hash={res['content_hash']}")

if __name__ == "__main__":
    main()
