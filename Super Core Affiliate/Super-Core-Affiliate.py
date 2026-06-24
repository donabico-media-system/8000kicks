#!/usr/bin/env python3
# Super-Core-Affiliate.py
# EATHESEN V3000-Ω | Self-Contained Drone Landing Page Engine
# Chiến thuật: Tự trị hoàn toàn, loại bỏ 404, tối ưu SEO 8000kicks

import os
import jinja2
from datetime import datetime
from typing import TypedDict, Annotated, Literal
from operator import add
from langgraph.graph import StateGraph, START, END

# ==================== CẤU HÌNH ĐỊNH DANH HỆ THỐNG ====================
class AffiliateState(TypedDict):
    niche: str
    research_data: dict
    optimized_copy: str
    html_content: str

# ==================== BỘ MÁY TỰ TRỊ (AGENTS) ====================
def researcher_node(state: AffiliateState):
    # Tự động hóa quét thị trường (Local Cache Mode)
    return {"research_data": {"trend": "Drone + 8000kicks Hybrid 2026", "cvr": "8.2%"}}

def copywriter_node(state: AffiliateState):
    return {"optimized_copy": "<h1>Sải cánh cùng 8000kicks - Drone Hybrid Thế hệ mới 2026</h1><p>Trải nghiệm công nghệ bay tiên phong...</p>"}

def renderer_node(state: AffiliateState):
    # TỰ GHI ĐÈ INDEX.HTML TẠI GỐC KHO 8000KICKS (LOẠI BỎ MỌI LỖI MẠNG)
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>8000kicks x Drone SOTA</title>
        <style>
            body { font-family: 'Times New Roman', serif; border: 4px solid #00ff66; padding: 20px; }
            .content { max-width: 800px; margin: auto; }
        </style>
    </head>
    <body>
        <div class="content">{{ content|safe }}</div>
        <footer style="margin-top:50px; text-align:center;">
            © 2026 8000kicks Super Core Affiliate | Autonomous Mode
        </footer>
    </body>
    </html>
    """
    html = jinja2.Template(template).render(content=state["optimized_copy"])
    
    # Định vị file theo cấu trúc cây thư mục của Admin
    output_path = os.path.join(os.getcwd(), "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return {"html_content": html}

# ==================== BUILD GRAPH (ENGINE BỘ NÃO) ====================
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
    print("🚀 [LOCAL-DRONE-CORE] Đang khởi chạy quy trình tự động hóa...")
    initial_state = {"niche": "8000kicks-Drone-Hybrid"}
    app_graph.invoke(initial_state)
    print("✅ [SUCCESS] Landing Page đã được cập nhật tại gốc kho 8000kicks.")
    
