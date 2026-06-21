#!/usr/bin/env python3
# Super-Core-Affiliate.py
# Path: Super Core Affiliate/Super-Core-Affiliate.py
# EATHESEN V3000-Ω | Drone Landing Page Affiliate 8000kicks
# CHẠY TRÊN GITHUB ACTIONS (Chrome) HOÀN TOÀN
# Keys (nếu cần) load từ GitHub Secrets hoặc Kho 4

import os
from datetime import datetime
from typing import TypedDict, Annotated, Literal
from operator import add
from langgraph.graph import StateGraph, START, END
import jinja2

# ==================== STATE & AGENTS (Drone + 8000kicks SOTA) ====================
class AffiliateState(TypedDict):
    messages: Annotated[list, add]
    niche: str
    research_data: dict
    copy_draft: str
    optimized_copy: str
    html_content: str
    affiliate_links: dict
    next: Literal["researcher", "copywriter", "optimizer", "renderer", "__end__"]

def researcher_node(state: AffiliateState):
    research = {
        "niche": state.get("niche", "Drone + 8000kicks Premium Affiliate 2026"),
        "trending": ["DJI Mavic 4 Pro", "Skydio 2+ Enterprise", "FPV x Kicks Collaboration 2026"],
        "conversion_benchmarks": "6.6% median CVR | Drone storytelling + high-ticket affiliate",
        "drone_benchmarks": "Flixar/Droney Gantt, Lunares single-screen, AeroControl SaaS, Pix4D AR"
    }
    return {"research_data": research, "next": "copywriter", "messages": state.get("messages", []) + ["Drone research complete"]}

def copywriter_node(state: AffiliateState):
    draft = """
    <h1>Drone Kicks 2026 – Limited Collaboration Drops</h1>
    <p>Premium drone performance meets street style. Only the best pairs for pilots & creators.</p>
    <!-- MID AFFILIATE ANCHOR -->
    """
    return {"copy_draft": draft, "next": "optimizer"}

def optimizer_node(state: AffiliateState):
    draft = state["copy_draft"]
    optimized = draft.replace("<!-- MID AFFILIATE ANCHOR -->", 
        '<a href="https://your-drone-mid-link.com" class="cta-mid" style="display:inline-block;background:#c00;color:#fff;padding:14px 32px;border-radius:8px;text-decoration:none;font-weight:bold;margin:20px 0;">Shop Mid Drone Offer →</a>') + """
    <div class="fomo" style="background:#c00;color:#fff;padding:14px;border-radius:8px;margin:30px 0;text-align:center;font-weight:bold;">
        🔥 Only 47 pairs left! "Vừa có khách hàng mua" – Order within 3 minutes
    </div>
    <a href="https://your-drone-bottom-link.com" class="cta-bottom" style="display:block;background:#000;color:#fff;padding:18px;text-align:center;border-radius:10px;text-decoration:none;font-size:1.1rem;font-weight:bold;margin-top:20px;">
        Claim Your Pair Now – Bottom CTA →
    </a>
    """
    affiliate_links = {
        "mid": "https://your-drone-mid-link.com",
        "bottom": "https://your-drone-bottom-link.com"
    }
    return {"optimized_copy": optimized, "affiliate_links": affiliate_links, "next": "renderer"}

def renderer_node(state: AffiliateState):
    template = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Drone 8000kicks 2026 | Premium Affiliate</title>
    <style>
        body { font-family: "Times New Roman", serif; background:#0B0D17; color:#fff; max-width:960px; margin:0 auto; padding:60px 20px; line-height:1.6; }
        .cta-mid:hover, .cta-bottom:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
    </style>
</head>
<body>
    {{ content }}
    <footer style="margin-top:80px; text-align:center; opacity:0.6; font-size:0.95rem;">
        © 2026 8000kicks Super Core Affiliate • Powered by EATHESEN V3000-Ω + Kho 4 + NGROK
    </footer>
</body>
</html>"""
    html = jinja2.Template(template).render(content=state["optimized_copy"])
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return {"html_content": html, "next": "__end__"}

# ==================== BUILD GRAPH ====================
workflow = StateGraph(AffiliateState)
workflow.add_node("researcher", researcher_node)
workflow.add_node("copywriter", copywriter_node)
workflow.add_node("optimizer", optimizer_node)
workflow.add_node("renderer", renderer_node)
workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", "copywriter")
workflow.add_edge("copywriter", "optimizer")
workflow.add_edge("optimizer", "renderer")
workflow.add_edge("renderer", END)
app_graph = workflow.compile()

if __name__ == "__main__":
    print("🚀 Generating Drone Landing Page Affiliate 8000kicks (EATHESEN V3000-Ω)...")
    initial = {"niche": "Drone + 8000kicks Premium Affiliate 2026", "messages": []}
    result = app_graph.invoke(initial)
    print("✅ index.html generated successfully!")
    print("Messages:", result.get("messages", []))