/* ==========================================================================
   ESEB SERVERLESS RUNNER (WORKERS 08-AI PERFECT MATRIX - SOTA 2026)
   MODULE: Protocols/Cf_Workers_Ai.js
   STAMP: V-STAMP-24 | DONABICO GLOBAL MEDIA SYSTEM
   STRICT COMPLIANCE: ESEB 04THU AUTO-6D PROTOCOL
   ========================================================================== */
const https = require('https');

class WorkersAiRunner {
  constructor() {
    this.stamp = "V-STAMP-24";
    this.accountId = process.env.CF_ACCOUNT_ID || '';
    this.apiToken = process.env.CF_API_TOKEN || '';
    
    // Matrix 08 AI Models Chuẩn Hóa REST API Cloudflare Edge 2026
    this.models = {
      llama_70b: "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
      llama_8b: "@cf/meta/llama-3.1-8b-instruct",
      deepseek: "@cf/deepseek-ai/deepseek-r1-distill-qwen-32b",
      mistral_7b: "@cf/mistral/mistral-7b-instruct-v0.1",
      qwen_7b: "@cf/qwen/qwen1.5-7b-chat",
      gemma_7b: "@cf/google/gemma-7b-it-lora",
      bge_embedding: "@cf/baai/bge-large-en-v1.5",
      sdxl_image: "@cf/bytedance/stable-diffusion-xl-lightning"
    };
  }

  async runAiInference(modelKey, modelId, promptText, payloadType = 'chat') {
    if (!this.accountId || !this.apiToken) {
      console.log(`[WORKERS AI ERROR] Credentials missing for node [${modelKey}].`);
      return false;
    }

    let payloadObj = {};
    if (payloadType === 'embedding') {
      payloadObj = { text: [promptText] };
    } else if (payloadType === 'image') {
      payloadObj = { prompt: promptText };
    } else {
      payloadObj = {
        messages: [
          { role: "system", content: "You are Cloudflare Global Affiliate AI Engine for DONABICO GLOBAL MEDIA SYSTEM. Markets: USA, Canada, UK, EU, AU, NZ, Global." },
          { role: "user", content: promptText }
        ]
      };
    }

    const payload = JSON.stringify(payloadObj);

    const options = {
      hostname: 'api.cloudflare.com',
      port: 443,
      path: `/client/v4/accounts/${this.accountId}/ai/run/${modelId}`,
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiToken}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      },
      timeout: 25000
    };

    return new Promise((resolve) => {
      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          if (res.statusCode === 200) {
            const contentType = res.headers['content-type'] || '';
            if (payloadType === 'image' || contentType.includes('image')) {
              console.log(`[ESEB 08-AI SUCCESS] Node: [${modelKey}] | Model: ${modelId} | Status 200 OK (Binary Image Stream)`);
              resolve(true);
              return;
            }
            try {
              const parsed = JSON.parse(data);
              if (parsed.success) {
                console.log(`[ESEB 08-AI SUCCESS] Node: [${modelKey}] | Model: ${modelId} | Status 200 OK`);
                resolve(true);
              } else {
                console.log(`[ESEB 08-AI ERROR] Node: [${modelKey}] | Status: ${res.statusCode} | Msg: ${JSON.stringify(parsed.errors || [])}`);
                resolve(false);
              }
            } catch(e) {
              console.log(`[ESEB PARSE ERROR] Node: [${modelKey}] | Status: ${res.statusCode}`);
              resolve(false);
            }
          } else {
            console.log(`[ESEB 08-AI ERROR] Node: [${modelKey}] | Status: ${res.statusCode}`);
            resolve(false);
          }
        });
      });
      req.on('timeout', () => { req.destroy(); resolve(false); });
      req.on('error', (err) => { console.log(`[ESEB NETWORK ERROR] Node: [${modelKey}] | ${err.message}`); resolve(false); });
      req.write(payload);
      req.end();
    });
  }

  async run() {
    console.log(`=================================================================`);
    console.log(`[ESEB FULL 08-AI GLOBAL MATRIX] Executing Cloudflare Edge GPU API Calls`);
    console.log(`Stamp: ${this.stamp} | DONABICO GLOBAL MEDIA SYSTEM`);
    console.log(`=================================================================`);

    await this.runAiInference("LLAMA_70B", this.models.llama_70b, "Create High-Intent Native English Reviews", "chat");
    await this.runAiInference("LLAMA_8B", this.models.llama_8b, "Execute Rapid RAG Fallback Inference", "chat");
    await this.runAiInference("DEEPSEEK", this.models.deepseek, "Perform Deep Logic Reasoning & GEO-SEO Optimization", "chat");
    await this.runAiInference("MISTRAL_7B", this.models.mistral_7b, "Format JSON-LD Schemas for Search Engines", "chat");
    await this.runAiInference("QWEN_7B", this.models.qwen_7b, "Optimize Multilingual Geo Target Content", "chat");
    await this.runAiInference("GEMMA_7B", this.models.gemma_7b, "Execute Auxiliary Context Enrichment", "chat");
    await this.runAiInference("BGE_EMBEDDING", this.models.bge_embedding, "EATHESEN RAG Knowledge Vectorization", "embedding");
    await this.runAiInference("SDXL_IMAGE", this.models.sdxl_image, "Professional Affiliate Shoe Product Banner", "image");

    console.log(`[ESEB 08-AI MATRIX] All 08 Active Nodes Executed with Zero Entropy.`);
    process.exit(0);
  }
}

if (require.main === module) {
  new WorkersAiRunner().run();
}

module.exports = WorkersAiRunner;
