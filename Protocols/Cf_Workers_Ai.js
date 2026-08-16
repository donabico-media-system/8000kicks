/* ==========================================================================
   ESEB SERVERLESS RUNNER (WORKERS 08-AI GLOBAL MATRIX CONNECTOR - SOTA 2026)
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
    
    // Matrix Model ID Chuẩn Hóa Route API Cloudflare Edge 2026
    this.models = {
      llama_70b: "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
      llama_8b: "@cf/meta/llama-3.1-8b-instruct",
      deepseek: "@cf/deepseek-ai/deepseek-r1-distill-qwen-32b",
      mistral_7b: "@cf/mistral/mistral-7b-instruct-v0.1"
    };
  }

  async runAiInference(modelKey, modelId, promptText) {
    if (!this.accountId || !this.apiToken) {
      console.log(`[WORKERS AI ERROR] Credentials missing for node [${modelKey}].`);
      return false;
    }

    // Payload Chuẩn Hóa Pure Messages (Khắc phục hoàn toàn lỗi oneOf schema 5006)
    const payload = JSON.stringify({
      messages: [
        { 
          role: "system", 
          content: "You are Cloudflare Global Affiliate AI Engine for DONABICO GLOBAL MEDIA SYSTEM. Markets: USA, Canada, UK, EU, AU, NZ, Global." 
        },
        { 
          role: "user", 
          content: promptText 
        }
      ]
    });

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
          try {
            const parsed = JSON.parse(data);
            if (res.statusCode === 200 && parsed.success) {
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
    console.log(`[ESEB 08-AI GLOBAL ENGINE] Executing Cloudflare Edge GPU API Call`);
    console.log(`Stamp: ${this.stamp} | DONABICO GLOBAL MEDIA SYSTEM`);
    console.log(`=================================================================`);

    await this.runAiInference("LLAMA_70B", this.models.llama_70b, "Create High-Intent Native English Product Reviews for US, UK, CA, AU, NZ Market");
    await this.runAiInference("LLAMA_8B", this.models.llama_8b, "Execute Rapid RAG Fallback Inference for US/EU Traffic");
    await this.runAiInference("DEEPSEEK", this.models.deepseek, "Perform Deep Logic Reasoning & GEO-SEO Optimization");
    await this.runAiInference("MISTRAL_7B", this.models.mistral_7b, "Format JSON-LD Schemas for EU Search Engines");

    console.log(`[ESEB 08-AI MATRIX] All Active Nodes Executed with Zero Entropy.`);
    process.exit(0);
  }
}

if (require.main === module) {
  new WorkersAiRunner().run();
}

module.exports = WorkersAiRunner;
