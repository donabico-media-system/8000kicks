#!/usr/bin/env python3
import os
import jinja2
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# State lưu trữ của Drone Core
class AffiliateState(TypedDict):
    niche: str
    optimized_copy: str

def researcher_node(state: AffiliateState):
    return {"niche": "8000kicks-Drone-Hybrid-2026"}

def copywriter_node(state: AffiliateState):
    return {"optimized_copy": "<h1>Sải cánh cùng 8000kicks</h1><p>Công nghệ Drone SOTA 2026.</p>"}

def renderer_node(state: AffiliateState):
    template = """
    <!DOCTYPE html>
    <html>
    <body>
        {{ content|safe }}
        <footer style="margin-top:50px;">© 2026 8000kicks Autonomous Core</footer>
    </body>
    </html>
    """
    html = jinja2.Template(template).render(content=state["optimized_copy"])
    
    # ĐỊNH VỊ GỐC KHO: Ghi đè vào index.html tại thư mục gốc của repo
    output_path = os.path.join(os.getcwd(), "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return {}

# Build Graph
workflow = StateGraph(AffiliateState)
workflow.add_node("researcher", researcher_node)
workflow.add_node("copywriter", copywriter_node)
workflow.add_node("renderer", renderer_node)

workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", "copywriter")
workflow.add_edge("copywriter", "renderer")
workflow.add_edge("renderer", END)

app_graph = workflow.compile()

if __name__ == "__main__":
    app_graph.invoke({"niche": "drone"})
    print("✅ [SUCCESS] Landing page đã được cập nhật tại gốc kho.")
    
