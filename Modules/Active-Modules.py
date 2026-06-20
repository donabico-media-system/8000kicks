#!/usr/bin/env python3
"""
EATHESEN V3000-Ω | AUTONOMOUS MATRIX INJECTOR v2 (Multi-Brand Scale Ready)
"""
import os
import re
import sys
import getopt
import concurrent.futures
from datetime import datetime, timezone
from collections import defaultdict

def get_protocols_from_file(module_file):
    try:
        with open(module_file, "r", encoding="utf-8") as f:
            content = f.read()
        if "PROTOCOLS = [" in content:
            start = content.find("PROTOCOLS = [") + len("PROTOCOLS = [")
            end = content.find("]", start)
            protocols_str = content[start:end]
            return [p.strip().strip("'\"") for p in protocols_str.split(",") if p.strip()]
    except:
        pass
    return []

def execute_single_module(module_file, target_url):
    if module_file == "Active-Modules.py":
        return None, []
    try:
        cmd = f"'{sys.executable}' '{module_file}' --url '{target_url}' > /dev/null 2>&1"
        exit_code = os.system(cmd)
        protocols = get_protocols_from_file(module_file)
        
        if exit_code == 0:
            return f"✅ {module_file}", protocols
        else:
            return f"❌ {module_file}", protocols
    except Exception as e:
        return f"💥 {module_file} -> {str(e)}", []

def run_massive_siphon_matrix(target_url, target_kho=""):
    print(f"[V3000-Ω] === EATHESEN MATRIX ACTIVATION FOR: {target_kho or 'Default'} ===")
    all_files = os.listdir(".")
    module_targets = [f for f in all_files if f.endswith(".py") and f != "Active-Modules.py"]
    
    print(f"[V3000-Ω] Tổng module phát hiện: {len(module_targets)}")
    print("-" * 70)

    results = []
    protocol_groups = defaultdict(list)

    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor:
        futures = {executor.submit(execute_single_module, mod, target_url): mod for mod in module_targets}
        for future in concurrent.futures.as_completed(futures):
            status, protocols = future.result()
            if status:
                print(status)
                for p in protocols:
                    print(f"   ✅ {p}")
                    if "Google" in p: protocol_groups["Google"].append(p)
                    elif any(x in p for x in ["Bing", "Microsoft"]): protocol_groups["Bing/Microsoft"].append(p)
                    elif any(x in p for x in ["Facebook", "Meta", "Instagram"]): protocol_groups["Meta/Social"].append(p)
                    elif "TikTok" in p: protocol_groups["TikTok"].append(p)
                    elif any(x in p for x in ["Affiliate", "Amazon", "CJ", "Impact"]): protocol_groups["Affiliate"].append(p)
                    else: protocol_groups["Other"].append(p)
                results.append((status, protocols))

    print("-" * 70)
    print("[V3000-Ω] TỔNG KẾT THEO NHÓM:")
    for group, protos in protocol_groups.items():
        print(f"  {group}: {len(protos)} giao thức ✅")

    return results, protocol_groups

def inject_production_html(results, protocol_groups, target_kho=""):
    index_path = os.path.join("..", "index.html")
    if not os.path.exists(index_path):
        index_path = "index.html"
    if not os.path.exists(index_path):
        print("[ERROR] Không tìm thấy index.html!")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # DỌN SẠCH TOÀN BỘ BANNER CŨ
    html = re.sub(r'<div id="dnbc-adtech-banner".*?</div>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<div id="eath esen-matrix-summary".*?</div>', '', html, flags=re.DOTALL | re.IGNORECASE)

    # Golden 2px Drone Shield (nếu bạn muốn giữ)
    golden_style = """
    <style>
    .drone-frame, #drone-main, .hero-drone, img[alt*="drone"] {
        border: 2px solid #FFD700 !important;
        box-shadow: 0 0 15px #FFD700, 0 0 25px #FFAA00 !important;
        animation: golden-glow 2s infinite alternate;
    }
    @keyframes golden-glow { from { box-shadow: 0 0 10px #FFD700; } to { box-shadow: 0 0 20px #FFAA00; } }
    </style>
    """
    if "<head>" in html:
        html = html.replace("<head>", f"<head>\n{golden_style}")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("[SUCCESS] Golden 2px Drone Shield injected (NO public banner)!")

if __name__ == "__main__":
    target_url = "https://donabico-global-media.github.io/8000kicks/"
    target_kho = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:k:", ["url=", "kho="])
        for opt, arg in opts:
            if opt in ("-u", "--url"): target_url = arg
            elif opt in ("-k", "--kho"): target_kho = arg
    except getopt.GetoptError:
        pass

    results, protocol_groups = run_massive_siphon_matrix(target_url, target_kho)
    inject_production_html(results, protocol_groups, target_kho)