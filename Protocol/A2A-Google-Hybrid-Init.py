import os
import httpx
import asyncio
from typing import Optional

class A2AHybridAgent:
    def __init__(self):
        self.gateway_url = os.getenv("CLOUDFLARE_AI_GATEWAY_URL", "https://ai-gateway.cloudflare.com")
        self.api_key = os.getenv("GOOGLE_API_KEY")

    async def execute_swarm_decision(self, task: str) -> Optional[Dict]:
        """Logic Hybrid: Kết hợp logic tại chỗ và AI Decisioning"""
        if not self.api_key:
            return {"error": "Authentication Failed: Missing API Key"}
            
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    f"{self.gateway_url}/v1beta/models/gemini-pro:streamGenerateContent",
                    headers={"x-goog-api-key": self.api_key},
                    json={"contents": [{"parts": [{"text": f"Analyze: {task}"}]}]}
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                return {"error": str(e)}

a2a_agent = A2AHybridAgent()
