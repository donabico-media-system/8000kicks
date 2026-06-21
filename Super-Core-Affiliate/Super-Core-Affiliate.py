# Super-Core-Affiliate.py
# Path: 8000kicks/Super Core Affiliate/Super-Core-Affiliate.py
# EATHESEN V3000-Ω | SOTA Affiliate Marketing System | LangGraph Multi-Agent
# Output: index.html (direct connection) | Times New Roman | 2x AFFILIATE_ANCHOR | FOMO

import os
from datetime import datetime
from typing import TypedDict, Annotated, Literal
from operator import add
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
import jinja2  # For clean HTML template

# State definition (shared across agents)
class AffiliateState(TypedDict):
    messages: Annotated[list, add]
    niche: str
    research_data: dict
    copy_draft: str
    optimized_copy: str
    html_content: str
    affiliate_links: dict
    next: Literal["researcher", "copywriter", "optimizer", "renderer", "__end__"]

# Agent 1: Researcher (Siphon competitor + niche data)
def researcher_node(state: AffiliateState):
    # Simulate SOTA research (integrate with real APIs or local siphon later)
    research = {
        "niche": state["niche"] or "Premium Sneakers & Kicks 2026",
        "trending": ["Nike Air Max 2026", "Adidas Ultraboost", "New Balance 9060"],
        "conversion_benchmarks": "6.6% median | Short copy +13% lift",
        "competitor_insights": "High-intent red-black CTAs win"
    }
    return {"research_data": research, "next": "copywriter", "messages": state["messages"] + ["Research complete"]}

# Agent 2: Copywriter (PAS + AIDA hybrid)
def copywriter_node(state: AffiliateState):
    research = state["research_data"]
    draft = f"""
    <h1>Discover the Hottest Kicks of 2026 – Limited Drops</h1>
    <p>Don't miss out on the sneakers everyone's talking about. 
    Premium comfort, style, and performance in one pair.</p>
    <!-- MID AFFILIATE ANCHOR PLACEHOLDER -->
    """
    return {"copy_draft": draft, "next": "optimizer", "messages": state["messages"] + ["Copy drafted"]}

# Agent 3: Optimizer (CRO + 2x anchors + FOMO)
def optimizer_node(state: AffiliateState):
    draft = state["copy_draft"]
    optimized = draft.replace(
        "<!-- MID AFFILIATE ANCHOR PLACEHOLDER -->",
        '<a href="https://your-affiliate-link-mid.com" class="cta-mid" style="color:#fff;background:#c00;padding:12px 24px;border-radius:6px;text-decoration:none;">Shop Mid Offer Now →</a>'
    ) + """
    <div class="fomo">🔥 Just 47 pairs left! "Vừa có khách hàng mua" – Order in 3 minutes.</div>
    <a href="https://your-affiliate-link-bottom.com" class="cta-bottom" style="display:block;margin-top:30px;color:#fff;background:#000;padding:16px;text-align:center;border-radius:8px;text-decoration:none;">Claim Your Pair at Bottom CTA →</a>
    """
    affiliate_links = {
        "mid": "https://your-affiliate-link-mid.com",
        "bottom": "https://your-affiliate-link-bottom.com"
    }
    return {"optimized_copy": optimized, "affiliate_links": affiliate_links, "next": "renderer"}

# Agent 4: Renderer (Direct index.html generation)
def renderer_node(state: AffiliateState):
    template = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Super Core Kicks 2026 | Premium Affiliate</title>
        <style>
            body { font-family: "Times New Roman", serif; background:#0B0D17; color:#fff; max-width:960px; margin:0 auto; padding:40px; }
            .cta-mid, .cta-bottom { transition: all 0.3s; }
            .cta-mid:hover, .cta-bottom:hover { transform: scale(1.05); }
            .fomo { background:#c00; padding:12px; border-radius:6px; margin:20px 0; text-align:center; }
        </style>
    </head>
    <body>
        {{ content }}
        <footer style="margin-top:60px; font-size:0.9em; opacity:0.7;">
            © 2026 Super Core Affiliate | Powered by EATHESEN V3000-Ω
        </footer>
    </body>
    </html>
    """
    html = jinja2.Template(template).render(content=state["optimized_copy"])
    
    # Direct write to index.html in repo root or /docs for GitHub Pages
    output_path = "index.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    return {"html_content": html, "next": "__end__", "messages": state["messages"] + [f"index.html generated at {datetime.now()}"]}

# Build the Graph
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

# Compile
app = workflow.compile()

# Run example
if __name__ == "__main__":
    initial_state = {"niche": "8000kicks Premium Sneakers Affiliate 2026", "messages": []}
    result = app.invoke(initial_state)
    print("✅ Super Core Affiliate completed. index.html generated.")
    print("Messages:", result["messages"])
