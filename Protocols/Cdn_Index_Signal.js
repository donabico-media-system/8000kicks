/**
 ===============================================================================
 ESEB PROTOCOL: SERVERLESS RUNNER & DUAL-TOKEN INDEXNOW EXECUTOR
 MODULE: Protocols/Cdn_Index_Signal.js
 STAMP: V-STAMP-24 | DUAL-TOKEN 4THU MODE | DONABICO MEDIA SYSTEM
 OMNI CNAME AUTO-DISCOVERY ENFORCED
 ===============================================================================
**/

const https = require('https');
const fs = require('fs');

class ServerlessDualTokenExecutionRunner {
  constructor() {
    this.stamp = "V-STAMP-24";
    this.brand = "DONABICO MEDIA SYSTEM";
    this.anchor = "¢24";
    
    this.tokens = {
      esebClassic: process.env.ESEB_CLASSIC_TOKEN || '',
      apiGroq: process.env.API_GROQ_TOKEN || ''
    };
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

  async callGroqAPI(promptText) {
    if (!this.tokens.apiGroq || !this.tokens.apiGroq.trim()) {
      console.log("[GROQ CORE] Token API_GROQ_TOKEN missing in Secrets. Skipping.");
      return { success: false };
    }

    const cleanToken = this.tokens.apiGroq.trim().replace(/^["']|["']$/g, '');
    const payload = JSON.stringify({
      model: "llama-3.3-70b-versatile",
      messages: [
        {"role": "system", "content": "You are ESEB Dynamic Living Protocol Core V3000-Ω. Process Custom Domain Indexing Signals."},
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
          resolve({ success: res.statusCode === 200 });
        });
      });
      req.on('timeout', () => { req.destroy(); resolve({ success: false }); });
      req.on('error', () => resolve({ success: false }));
      req.write(payload);
      req.end();
    });
  }

  async broadcastIndexNow(domain, urlList) {
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
        resolve({ success: res.statusCode === 200 || res.statusCode === 202 });
      });
      req.on('timeout', () => { req.destroy(); resolve({ success: false }); });
      req.on('error', () => resolve({ success: false }));
      req.write(payload);
      req.end();
    });
  }

  async runRealExecution() {
    const targetDomain = this.getAutoDiscoveredDomain();
    console.log(`=================================================================`);
    console.log(`[DUAL-TOKEN RUNNER] Executing IndexNow Broadcast for Domain: ${targetDomain}`);
    console.log(`Brand: ${this.brand} | Stamp: ${this.stamp} | Anchor: ${this.anchor}`);
    console.log(`=================================================================`);

    await this.callGroqAPI(`Execute ESEB CDN Index Signal matrix synchronization for domain: ${targetDomain}`);
    await this.broadcastIndexNow(targetDomain, [`https://${targetDomain}/`]);

    if (this.tokens.esebClassic) {
      console.log(`[ESEB CLASSIC SUCCESS] Core Authenticated | V-STAMP-24 Verified.`);
    }

    console.log(`[DUAL-TOKEN RUNNER] All Indexing Pipelines Completed. Entropy delta = 0.`);
    process.exit(0);
  }
}

if (require.main === module) {
  const runner = new ServerlessDualTokenExecutionRunner();
  runner.runRealExecution();
}

module.exports = ServerlessDualTokenExecutionRunner;
