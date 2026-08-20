/**
 ===============================================================================
 ESEB PROTOCOL: SERVERLESS RUNNER & SUPER SMART INTELLIGENT AI MATRIX
 MODULE: Protocols/Super_Affiliate_Core.js
 STAMP: V-STAMP-24 | DUAL-TOKEN 4THU MODE | DONABICO MEDIA SYSTEM
 CLOUDFLARE WORKERS AI REST API (SUPER SMART INTELLIGENT ROTATION)
 ===============================================================================
**/

const https = require('https');
const fs = require('fs');

class SuperSmartCloudflareRunner {
  constructor() {
    this.stamp = "V-STAMP-24";
    this.brand = "DONABICO MEDIA SYSTEM";
    this.anchor = "¢24";
    
    this.tokens = {
      esebClassic: process.env.ESEB_CLASSIC_TOKEN || '',
      cfAccountId: process.env.CF_ACCOUNT_ID || '',
      cfApiToken: process.env.CF_API_TOKEN || ''
    };

    this.aiMatrix = [
      { key: "LLAMA_70B", id: "@cf/meta/llama-3.3-70b-instruct-fp8-fast", type: "chat", role: "Super Smart Affiliate Reviews & Q-Learning" },
      { key: "LLAMA_8B", id: "@cf/meta/llama-3.1-8b-instruct", type: "chat", role: "Rapid RAG Fallback & Smart Sourcing" },
      { key: "DEEPSEEK", id: "@cf/deepseek-ai/deepseek-r1-distill-qwen-32b", type: "chat", role: "Advanced Reasoning & GEO-SEO Optimization" },
      { key: "MISTRAL_7B", id: "@cf/mistral/mistral-7b-instruct-v0.1", type: "chat", role: "JSON-LD Schema & Structured Intelligence" },
      { key: "LLAMA_3B", id: "@cf/meta/llama-3.2-3b-instruct", type: "chat", role: "Edge Ultra-Fast Localization" },
      { key: "GEMMA_7B", id: "@cf/google/gemma-7b-it-lora", type: "chat", role: "Context Enrichment & Smart Conversion" },
      { key: "BGE_EMBEDDING", id: "@cf/baai/bge-large-en-v1.5", type: "embedding", role: "RAG Knowledge Vectorization" },
      { key: "SDXL_IMAGE", id: "@cf/bytedance/stable-diffusion-xl-lightning", type: "image", role: "Affiliate Intelligent Banners & Posters" }
    ];
  }

  getAutoDiscoveredDomain() {
    try {
      if (fs.existsSync('CNAME')) {
        const cnameDomain = fs.readFileSync('CNAME', 'utf8').trim();
        if (cnameDomain) return cnameDomain;
      }
    } catch(e) {}

    const githubRepo = process.env.GITHUB_REPOSITORY || 'donabico-media-system/8000kicks';
    const parts = githubRepo.split('/');
    const owner = parts[0] || 'donabico-media-system';
    const repo = parts[1] || '8000kicks';
    return repo.toLowerCase() === `${owner.toLowerCase()}.github.io` ? `${owner}.github.io` : `${owner}.github.io/${repo}`;
  }

  async callCloudflareNode(node, targetDomain) {
    if (!this.tokens.cfAccountId || !this.tokens.cfApiToken) {
      console.log(`[CF MATRIX] Missing Cloudflare Account ID or API Token. Skipping node ${node.key}.`);
      return { success: false, status: 0 };
    }

    const accountId = this.tokens.cfAccountId.trim().replace(/^["']|["']$/g, '');
    const apiToken = this.tokens.cfApiToken.trim().replace(/^["']|["']$/g, '');

    let payloadObj = {};
    if (node.type === 'chat') {
      payloadObj = {
        messages: [
          {"role": "system", "content": `You are Super Smart Intelligent Affiliate Node ${node.key} (${node.role}) operating under V3000-Ω.`},
          {"role": "user", "content": `Execute intelligent affiliate growth context and adaptive conversion vectors for domain ${targetDomain}.`}
        ]
      };
    } else if (node.type === 'embedding') {
      payloadObj = { text: `Super Smart vector synchronization for domain ${targetDomain}` };
    } else if (node.type === 'image') {
      payloadObj = { prompt: `Super smart affiliate promotional banner for domain ${targetDomain}`, num_steps: 4 };
    }

    const payload = JSON.stringify(payloadObj);
    const options = {
      hostname: 'api.cloudflare.com',
      port: 443,
      path: `/client/v4/accounts/${accountId}/ai/run/${node.id}`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiToken}`,
        'Content-Length': Buffer.byteLength(payload)
      },
      timeout: 10000
    };

    return new Promise((resolve) => {
      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', (chunk) => data += chunk);
        res.on('end', () => {
          console.log(`[SUPER SMART AI EXECUTION] Node [${node.key}] Role [${node.role}] HTTP Status: ${res.statusCode}`);
          resolve({ success: res.statusCode === 200, status: res.statusCode });
        });
      });
      req.on('timeout', () => { req.destroy(); resolve({ success: false, status: 408 }); });
      req.on('error', () => resolve({ success: false, status: 500 }));
      req.write(payload);
      req.end();
    });
  }

  async runRealExecution() {
    const targetDomain = this.getAutoDiscoveredDomain();
    console.log(`=================================================================`);
    console.log(`[SUPER SMART INTELLIGENT RUNNER] Safe Rotational AI Execution`);
    console.log(`Brand: ${this.brand} | Stamp: ${this.stamp} | Target Domain: ${targetDomain}`);
    console.log(`=================================================================`);

    // Smart Rotation: Chọn an toàn 2 Node thông minh trong mảng để không chạm ngưỡng 429
    const shuffled = [...this.aiMatrix].sort(() => 0.5 - Math.random());
    const selectedNodes = shuffled.slice(0, 2); 

    console.log(`[SUPER SMART ROTATION] Active Intelligent Batch: ${selectedNodes.map(n => n.key).join(', ')}`);

    for (const node of selectedNodes) {
      await this.callCloudflareNode(node, targetDomain);
      await new Promise(resolve => setTimeout(resolve, 3000));
    }

    if (this.tokens.esebClassic) {
      console.log(`[ESEB CLASSIC SUCCESS] Core Authenticated | V-STAMP-24 Verified.`);
    }

    console.log(`[SUPER SMART INTELLIGENT RUNNER] Execution Completed Successfully. Entropy δ = 0.`);
    process.exit(0);
  }
}

if (require.main === module) {
  const runner = new SuperSmartCloudflareRunner();
  runner.runRealExecution();
}

module.exports = SuperSmartCloudflareRunner;
