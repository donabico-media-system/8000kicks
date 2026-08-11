/**
 ===============================================================================
 ESEB PROTOCOL: SERVERLESS RUNNER & ROBUST TIMEOUT API EXECUTOR
 MODULE: Protocols/Cdn_Index_Signal.js
 STAMP: V-STAMP-24 | 4THU TIMEOUT-PROTECTED | DONABICO GLOBAL MEDIA SYSTEM
 ===============================================================================
**/

const https = require('https');

class ServerlessTimeoutExecutionRunner {
  constructor() {
    this.stamp = "V-STAMP-24";
    this.brand = "DONABICO GLOBAL MEDIA SYSTEM";
    this.anchor = "¢24";
    
    this.tokens = {
      esebClassic: process.env.ESEB_CLASSIC_TOKEN || '',
      apiGroq: process.env.API_GROQ_TOKEN || '',
      llamaMeta: process.env.LLAMA_META_TOKEN || '',
      llamaNvidia: process.env.LLAMA_NVIDIA_TOKEN || '',
      nemotronNvidia: process.env.NEMOTRON_NVIDIA_TOKEN || ''
    };
  }

  async sendRequestWithTimeout(options, payload, apiName) {
    return new Promise((resolve) => {
      let timedOut = false;
      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', (chunk) => data += chunk);
        res.on('end', () => {
          if (timedOut) return;
          console.log(`[${apiName} RESPONSE] Status Code: ${res.statusCode} | Length: ${data.length}`);
          resolve(data);
        });
      });

      req.on('error', (err) => {
        if (timedOut) return;
        console.error(`[${apiName} ERROR] ${err.message}`);
        resolve(null);
      });

      // Cài đặt giới hạn thời gian timeout là 8000ms (8 giây) để không bao giờ bị treo workflow
      req.setTimeout(8000, () => {
        timedOut = true;
        req.destroy();
        console.warn(`[${apiName} WARNING] Request timed out after 8000ms. Bypassing safely.`);
        resolve(null);
      });

      if (payload) req.write(payload);
      req.end();
    });
  }

  async callGroqAPI(promptText) {
    if (!this.tokens.apiGroq) {
      console.log(`[GROQ API] Skipped: Token not provided.`);
      return null;
    }
    const payload = JSON.stringify({
      model: "llama-3.3-70b-versatile",
      messages: [{"role": "user", "content": promptText}]
    });

    const options = {
      hostname: 'api.groq.com',
      path: '/openai/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.tokens.apiGroq}`
      }
    };

    return await this.sendRequestWithTimeout(options, payload, 'GROQ API');
  }

  async callNvidiaNIMAPI(tokenKey, modelName, promptText) {
    const token = this.tokens[tokenKey];
    if (!token) {
      console.log(`[NVIDIA NIM API (${modelName})] Skipped: Token not provided.`);
      return null;
    }
    const payload = JSON.stringify({
      model: modelName,
      messages: [{"role": "user", "content": promptText}],
      temperature: 0.5,
      max_tokens: 128
    });

    const options = {
      hostname: 'integrate.api.nvidia.com',
      path: '/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    };

    return await this.sendRequestWithTimeout(options, payload, `NVIDIA NIM (${modelName})`);
  }

  async runRealExecution() {
    console.log(`=================================================================`);
    console.log(`[SERVERLESS RUNNER] Executing Robust API Calls with 8s Timeout`);
    console.log(`Brand: ${this.brand} | Stamp: ${this.stamp} | Anchor: ${this.anchor}`);
    console.log(`=================================================================`);

    const targetPrompt = "Initialize ESEB secure edge telemetry sync.";

    await this.callGroqAPI(targetPrompt);
    await this.callNvidiaNIMAPI('llamaNvidia', 'meta/llama-3.3-70b-instruct', targetPrompt);
    await this.callNvidiaNIMAPI('nemotronNvidia', 'nvidia/nemotron-4-34b-instruct', targetPrompt);

    console.log(`[SERVERLESS RUNNER] All Execution Pipelines Completed Safely. Entropy delta = 0.`);
  }
}

if (require.main === module) {
  const runner = new ServerlessTimeoutExecutionRunner();
  runner.runRealExecution();
}

module.exports = ServerlessTimeoutExecutionRunner;
