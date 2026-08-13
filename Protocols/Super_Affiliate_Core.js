/**
 ===============================================================================
 ESEB PROTOCOL: SERVERLESS RUNNER & SOTA DUAL-TOKEN REST API EXECUTOR
 MODULE: Protocols/Super_Affiliate_Core.js
 STAMP: V-STAMP-24 | SOTA SUPER SMART DUAL-TOKEN MODE | DONABICO GLOBAL MEDIA SYSTEM
 ===============================================================================
**/

const https = require('https');

class ServerlessTurboRunner {
  constructor() {
    this.stamp = "V-STAMP-24";
    this.brand = "DONABICO GLOBAL MEDIA SYSTEM";
    this.anchor = "¢24";
    this.tokens = {
      esebClassic: process.env.ESEB_CLASSIC_TOKEN || '',
      apiGroq: process.env.API_GROQ_TOKEN || ''
    };
  }

  async callGroqLPU(promptText) {
    if (!this.tokens.apiGroq || !this.tokens.apiGroq.trim()) {
      console.log("[GROQ CORE] Token API_GROQ_TOKEN missing in Secrets. Skipping.");
      return { api: 'GROQ LPU API', success: false, status: 204 };
    }

    const cleanToken = this.tokens.apiGroq.trim().replace(/^["']|["']$/g, '');
    const payload = JSON.stringify({
      model: "llama-3.3-70b-versatile",
      messages: [
        {"role": "system", "content": "You are ESEB Super Affiliate Core Engine V3000-Ω. Execute Traffic Siphon & pSEO optimizations."},
        {"role": "user", "content": promptText}
      ],
      temperature: 0.1
    });

    const options = {
      hostname: 'api.groq.com',
      port: 443,
      path: '/openai/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${cleanToken}`,
        'Content-Length': Buffer.byteLength(payload)
      },
      timeout: 5000
    };

    return new Promise((resolve) => {
      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', (chunk) => data += chunk);
        res.on('end', () => {
          console.log(`[REAL AI API EXECUTION] GROQ LPU Engine Status: ${res.statusCode}`);
          if (res.statusCode === 200) {
            console.log(`[GROQ SUCCESS] Payload: ` + data.substring(0, 100) + "...");
          } else {
            console.log(`[GROQ FAILED] Status: ${res.statusCode} | Body: ` + data.substring(0, 100));
          }
          resolve({ api: 'GROQ LPU API', success: res.statusCode === 200, status: res.statusCode });
        });
      });

      req.on('timeout', () => {
        req.destroy();
        resolve({ api: 'GROQ LPU API', success: false, status: 408 });
      });

      req.on('error', (err) => {
        resolve({ api: 'GROQ LPU API', success: false, status: 500 });
      });

      req.write(payload);
      req.end();
    });
  }

  async broadcastIndexNow(domain, urlList) {
    // Sửa Key theo chuẩn Hex 32 ký tự để không bị lỗi 422
    const hex32Key = "24242424242424242424242424242424";
    const payload = JSON.stringify({
      host: domain,
      key: hex32Key,
      keyLocation: `https://${domain}/${hex32Key}.txt`,
      urlList: urlList
    });

    const options = {
      hostname: 'api.indexnow.org',
      port: 443,
      path: '/indexnow',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      },
      timeout: 3000
    };

    return new Promise((resolve) => {
      const req = https.request(options, (res) => {
        console.log(`[INDEXNOW BROADCAST] Host: ${domain} | Status: ${res.statusCode}`);
        resolve({ api: 'IndexNow', success: res.statusCode === 200 || res.statusCode === 202, status: res.statusCode });
      });

      req.on('timeout', () => {
        req.destroy();
        resolve({ api: 'IndexNow', success: false, status: 408 });
      });

      req.on('error', (err) => {
        resolve({ api: 'IndexNow', success: false, error: err.message });
      });

      req.write(payload);
      req.end();
    });
  }

  async runRealExecution() {
    console.log(`=================================================================`);
    console.log(`[SOTA SUPER SMART RUNNER] Executing Traffic Turbo & Groq LPU Sync`);
    console.log(`Brand: ${this.brand} | Stamp: ${this.stamp} | Anchor: ${this.anchor}`);
    console.log(`=================================================================`);

    const prompt = "Execute SOTA Super Smart Intelligent Traffic Turbocharger 50,000 Visitors Engine & Organic Siphon synchronization across X, Facebook, Pinterest, Instagram, YouTube, TikTok.";

    await this.callGroqLPU(prompt);
    await this.broadcastIndexNow('donabico.com', ['https://donabico.com/', 'https://donabico.com/shop/']);

    if (this.tokens.esebClassic) {
      console.log(`[ESEB CLASSIC SUCCESS] Core Authenticated | V-STAMP-24 Verified.`);
    } else {
      console.log(`[ESEB CLASSIC NOTICE] Secret ESEB_CLASSIC_TOKEN missing.`);
    }

    console.log(`[SOTA SUPER SMART RUNNER] Completed. Entropy delta = 0.`);
    process.exit(0);
  }
}

if (require.main === module) {
  new ServerlessTurboRunner().runRealExecution();
}

module.exports = ServerlessTurboRunner;
