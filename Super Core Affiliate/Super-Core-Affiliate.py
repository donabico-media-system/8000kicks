#!/usr/bin/env python3
# Super-Core-Affiliate.py
# Path: Super Core Affiliate/Super-Core-Affiliate.py
# EATHESEN V3000-Ω | SOTA Affiliate Marketing System | LangGraph Multi-Agent
# Tự động generate index.html ở thư mục gốc repo (../index.html)

import os
from datetime import datetime
from typing import TypedDict, Annotated, Literal
from operator import add
from langgraph.graph import StateGraph, START, END
import jinja2

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
        "niche": state.get("niche", "8000kicks Premium Sneakers & Kicks 2026"),
        "trending": ["Nike Air Max 2026", "Adidas Ultraboost 2026", "New Balance 9060"],
        "conversion_benchmarks": "6.6% median CVR | Short copy +13% lift | High-intent red-black CTAs",
        "competitor_insights": "FOMO + 2 strategic affiliate anchors convert best"
    }
    return {
        "research_data": research,
        "next": "copywriter",
        "messages": state.get("messages", []) + ["Research complete - 8000kicks niche"]
    }

def copywriter_node(state: AffiliateState):
    research = state["research_data"]
    draft = f"""
    <h1 style="font-size:2.8rem; margin-bottom:20px;">Discover the Hottest Kicks of 2026</h1>
    <p style="font-size:1.2rem; max-width:700px; margin:0 auto 30px;">
        Premium comfort, style and performance. Limited drops you can't miss.
    </p>
    <!-- MID AFFILIATE ANCHOR -->
    """
    return {
        "copy_draft": draft,
        "next": "optimizer",
        "messages": state.get("messages", []) + ["Copy drafted with PAS/AIDA hybrid"]
    }

def optimizer_node(state: AffiliateState):
    draft = state["copy_draft"]
    optimized = draft.replace(
        "<!-- MID AFFILIATE ANCHOR -->",
        '<a href="https://your-affiliate-mid-link.com" target="_blank" class="cta-mid" style="display:inline-block; background:#c00; color:#fff; padding:14px 32px; border-radius:8px; text-decoration:none; font-weight:bold; margin:20px 0;">Shop Mid Offer Now →</a>'
    ) + """
    <div class="fomo" style="background:#c00; color:#fff; padding:14px; border-radius:8px; margin:30px 0; text-align:center; font-weight:bold;">
        🔥 Only 47 pairs left! "Vừa có khách hàng mua" – Order within 3 minutes
    </div>
    <a href="https://your-affiliate-bottom-link.com" target="_blank" class="cta-bottom" style="display:block; background:#000; color:#fff; padding:18px; text-align:center; border-radius:10px; text-decoration:none; font-size:1.1rem; font-weight:bold; margin-top:20px;">
        Claim Your Pair Now – Bottom CTA →
    </a>
    """
    affiliate_links = {
        "mid": "https://your-affiliate-mid-link.com",
        "bottom": "https://your-affiliate-bottom-link.com"
    }
    return {
        "optimized_copy": optimized,
        "affiliate_links": affiliate_links,
        "next": "renderer"
    }

def renderer_node(state: AffiliateState):
    template = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>8000kicks | Premium Sneakers Affiliate 2026</title>
    <style>
        body { font-family: "Times New Roman", serif; background:#0B0D17; color:#fff; max-width:960px; margin:0 auto; padding:60px 20px; line-height:1.6; }
        h1 { font-size:3rem; }
        .cta-mid:hover, .cta-bottom:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
        .fomo { animation: pulse 2s infinite; }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.85} }
    </style>
</head>
<body>
    {{ content }}
    <footer style="margin-top:80px; text-align:center; opacity:0.6; font-size:0.95rem;">
        © 2026 8000kicks Super Core Affiliate • Powered by EATHESEN V3000-Ω
    </footer>
</body>
</html>"""

    html = jinja2.Template(template).render(content=state["optimized_copy"])
    
    # FIX: Ghi file index.html ở thư mục gốc repo (../index.html)
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    return {
        "html_content": html,
        "next": "__end__",
        "messages": state.get("messages", []) + [f"index.html generated successfully at {datetime.now()}"]
    }

# Build Graph
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

app = workflow.compile()

if __name__ == "__main__":
    print("🚀 Starting Super Core Affiliate System (EATHESEN V3000-Ω)...")
    initial = {"niche": "8000kicks Premium Sneakers Affiliate 2026", "messages": []}
    result = app.invoke(initial)
    print("✅ Completed. Messages:", result["messages"])
