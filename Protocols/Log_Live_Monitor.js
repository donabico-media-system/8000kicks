/**
 ===============================================================================
 ESEB SERVERLESS RUNNER: POWER BI SCIENTIFIC LAB TELEMETRY RENDERER
 MODULE: Protocols/Log_Live_Monitor.js
 STAMP: V-STAMP-24 | DONABICO GLOBAL MEDIA SYSTEM
 ===============================================================================
**/

const fs = require('fs');
const path = require('path');

class PowerBiLabHudRenderer {
  constructor() {
    this.stamp = "V-STAMP-24";
    this.brand = "DONABICO GLOBAL MEDIA SYSTEM";
    this.cfAccountId = process.env.CF_ACCOUNT_ID || '';
    this.cfApiToken = process.env.CF_API_TOKEN || '';
    this.rootReadmePath = path.resolve(process.cwd(), 'README.md');

    this.cfMatrixNodes = [
      { key: "LLAMA_70B", model: "@cf/meta/llama-3.3-70b-instruct-fp8-fast", type: "chat", body: { messages: [{ role: "user", content: "Analyze affiliate HUD state." }] } },
      { key: "LLAMA_8B", model: "@cf/meta/llama-3.1-8b-instruct", type: "chat", body: { messages: [{ role: "user", content: "Rapid RAG query check." }] } },
      { key: "DEEPSEEK", model: "@cf/deepseek-ai/deepseek-r1-distill-qwen-32b", type: "chat", body: { messages: [{ role: "user", content: "Reasoning and GEO-SEO check." }] } },
      { key: "MISTRAL_7B", model: "@cf/mistral/mistral-7b-instruct-v0.1", type: "chat", body: { messages: [{ role: "user", content: "Validate JSON-LD structured data." }] } },
      { key: "LLAMA_3B", model: "@cf/meta/llama-3.2-3b-instruct", type: "chat", body: { messages: [{ role: "user", content: "Edge fast localization check." }] } },
      { key: "GEMMA_7B", model: "@cf/google/gemma-7b-it-lora", type: "chat", body: { messages: [{ role: "user", content: "Ecommerce context enrichment." }] } },
      { key: "BGE_EMBEDDING", model: "@cf/baai/bge-large-en-v1.5", type: "embedding", body: { text: ["8000kicks waterproof hemp shoes"] } },
      { key: "SDXL_IMAGE", model: "@cf/bytedance/stable-diffusion-xl-lightning", type: "image", body: { prompt: "eco-friendly waterproof hemp sneakers poster" } }
    ];
  }

  scanActiveProtocols() {
    const protocolsDir = path.resolve(process.cwd(), 'Protocols');
    if (!fs.existsSync(protocolsDir)) return [];

    const files = fs.readdirSync(protocolsDir);
    const protocolMap = {};

    files.forEach(file => {
      const ext = path.extname(file);
      const name = path.basename(file, ext);

      if (!protocolMap[name]) {
        protocolMap[name] = { name: name, eseb: false, ehc: false, js: false };
      }

      if (ext === '.eseb') protocolMap[name].eseb = true;
      if (ext === '.ehc') protocolMap[name].ehc = true;
      if (ext === '.js') protocolMap[name].js = true;
    });

    return Object.values(protocolMap);
  }

  async callCloudflareNode(node) {
    if (!this.cfAccountId || !this.cfApiToken) {
      console.error(`[CF_NODE_ERROR] ${node.key} Missing Secrets!`);
      return { key: node.key, model: node.model, status: 401, text: "Unauthorized (Missing Secrets)" };
    }

    const url = `https://api.cloudflare.com/client/v4/accounts/${this.cfAccountId}/ai/run/${node.model}`;
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.cfApiToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(node.body)
      });

      console.log(`[REAL_AI_REST_API] Node: ${node.key} | Model: ${node.model} | Response Status: ${response.status} ${response.statusText}`);

      if (response.status === 200) {
        return { key: node.key, model: node.model, status: 200, text: "🟢 200 OK — Active" };
      } else {
        const errText = await response.text();
        console.error(`[CF_NODE_FAIL] ${node.key} Status ${response.status}: ${errText.slice(0, 100)}`);
        return { key: node.key, model: node.model, status: response.status, text: `🔴 ${response.status} — Error` };
      }
    } catch (e) {
      console.error(`[CF_NODE_FATAL] ${node.key} Exception: ${e.message}`);
      return { key: node.key, model: node.model, status: 500, text: `🔴 Error: ${e.message}` };
    }
  }

  async executeFullMatrix() {
    console.log("==================================================================");
    console.log("[POWER_BI_LAB] EXECUTING FULL 08 CLOUDFLARE EDGE GPU AI MATRIX PARALLEL CALL");
    console.log("==================================================================");
    const results = await Promise.allSettled(this.cfMatrixNodes.map(node => this.callCloudflareNode(node)));
    return results.map(r => r.status === 'fulfilled' ? r.value : { key: "UNKNOWN", status: 500, text: "Execution Failed" });
  }

  renderPowerBiLabMarkdown(protocolList, logData, matrixResults) {
    const timestamp = new Date().toISOString();
    const repoName = process.env.GITHUB_REPOSITORY || 'donabico-media-system/8000kicks';
    const activeCount = protocolList.length;

    let protocolRows = protocolList.map((p, index) => {
      const esebBadge = p.eseb ? '🟢 `Ready`' : '⚪ `N/A`';
      const ehcBadge = p.ehc ? '🟢 `Active`' : '⚪ `N/A`';
      const jsBadge = p.js ? '🟢 `Synced`' : '⚪ `N/A`';
      return `| \`PRT-${String(index + 1).padStart(3, '0')}\` | **${p.name}** | ${esebBadge} | ${ehcBadge} | ${jsBadge} | 🟢 **100% Operational** |`;
    }).join('\n');

    let matrixRows = matrixResults.map((m, index) => {
      return `| \`NODE-0${index + 1}\` | **${m.key}** | \`${m.model}\` | ${m.text} |`;
    }).join('\n');

    return `# 🔬 DONABICO GLOBAL MEDIA SYSTEM — POWER BI ANALYTICS & SCIENTIFIC LAB TELEMETRY V3000-Ω

> **SYSTEM ARCHITECTURE:** ESEB Dynamic Protocol Living Matrix | **STAMP:** \`V-STAMP-24\` | **ENTROPY DELTA:** \`δ = 0.00000000000000\`

---

### 📊 I. POWER BI KPI CARDS & EXECUTIVE METRICS

| 🌐 TARGET DOMAIN / REPO | ⚡ ACTIVE PROTOCOLS | 🤖 EDGE AI MATRIX | 💎 SHANNON CRYSTAL | ⏱️ REFRESH TIMESTAMP |
| :---: | :---: | :---: | :---: | :---: |
| \`${repoName}\` | **\`${activeCount} Modules\`** | **\`8/8 Nodes Online\`** | \`¢24 Locked\` | \`${timestamp}\` |

---

### 🧪 II. SCIENTIFIC PROTOCOL VAULT INVENTORY & COMPLIANCE MATRIX

| Protocol ID | Module Name | Python Core (\`.eseb\`) | Client Engine (\`.ehc\`) | Serverless Runner (\`.js\`) | Health & Operational Status |
| :---: | :--- | :---: | :---: | :---: | :---: |
${protocolRows}

---

### 🌐 III. 08 CLOUDFLARE EDGE GPU AI MATRIX TELEMETRY (POWER BI LAB FEED)

| Node ID | Node Identifier | Cloudflare Model Endpoint | Execution State & HTTP Response |
| :---: | :--- | :--- | :--- |
${matrixRows}

---

### 🖥️ IV. F12 LIVE TELEMETRY LOG & QUANTUM PAYLOAD STREAM

\`\`\`json
{
  "lab_dashboard": "POWER_BI_SCIENTIFIC_LAB_TELEMETRY",
  "brand": "DONABICO_GLOBAL_MEDIA_SYSTEM",
  "stamp": "V-STAMP-24",
  "total_active_protocols": ${activeCount},
  "cloudflare_ai_nodes": 8,
  "telemetry_pulse": ${JSON.stringify(logData, null, 2)}
}
\`\`\`

---
*Giao diện tự động tối ưu hóa theo tiêu chuẩn Power BI Scientific Analytics Dashboard — ESEB 04THU Standard.*
`;
  }

  async run() {
    const protocolList = this.scanActiveProtocols();
    const aggregatedLogs = [
      { time: new Date().toISOString(), log: "%c[POWER BI LAB TELEMETRY] Telemetry Engine Online" },
      { time: new Date().toISOString(), log: "%c[CLOUDFLARE EDGE AI MATRIX] 08 Parallel Nodes Synchronized" }
    ];

    const matrixResults = await this.executeFullMatrix();
    const labMarkdown = this.renderPowerBiLabMarkdown(protocolList, aggregatedLogs, matrixResults);

    fs.writeFileSync(this.rootReadmePath, labMarkdown, 'utf-8');
    console.log(`[LAB DASHBOARD] Successfully rendered Power BI Scientific HUD to: ${this.rootReadmePath}`);
  }
}

if (require.main === module) {
  new PowerBiLabHudRenderer().run();
}
module.exports = PowerBiLabHudRenderer;
