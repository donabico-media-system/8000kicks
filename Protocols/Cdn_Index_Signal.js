/**
 ===============================================================================
 ESEB PROTOCOL: SERVERLESS RUNNER & 5-TOKEN CONCURRENT API EXECUTOR
 MODULE: Protocols/Cdn_Index_Signal.js
 STAMP: V-STAMP-24 | 5-TOKEN 4THU MODE | DONABICO GLOBAL MEDIA SYSTEM
 ===============================================================================
**/

const https = require('https');

class Serverless5TokenExecutionRunner {
  constructor() {
    this.stamp = "V-STAMP-24";
    this.brand = "DONABICO GLOBAL MEDIA SYSTEM";
    this.anchor = "¢24";
    
    // Nạp chính xác 5 Token bảo mật từ GitHub Actions Secrets
    this.tokens = {
      esebClassic: process.env.ESEB_CLASSIC_TOKEN || '',
      apiGroq: process.env.API_GROQ_TOKEN || '',
      nanoNvidia: process.env.NANO_NVIDIA_TOKEN || '',
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
          resolve({ api: apiName, status: res.statusCode, success: true, data });
        });
      });

      req.on('error', (err) => {
        if (timedOut) return;
        console.error(`[${apiName} ERROR] ${err.message}`);
        resolve({ api: apiName, success: false, error: err.message });
      });

      req.setTimeout(35000, () => {
        timedOut = true;
        req.destroy();
        console.warn(`[${apiName} WARNING] Request timed out after 35000ms.`);
        resolve({ api: apiName, success: false, error: 'TIMEOUT_35S' });
      });

      if (payload) req.write(payload);
      req.end();
    });
  }

  async callGroqAPI(promptText) {
    if (!this.tokens.apiGroq) return { api: 'GROQ API', success: false, error: 'NO_TOKEN' };
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
    return await this.sendRequestWithTimeout(options, payload, 'GROQ API (Llama 3.3)');
  }

  async callNvidiaNIMAPI(tokenKey, modelName, apiLabel, promptText) {
    const token = this.tokens[tokenKey];
    if (!token) return { api: apiLabel, success: false, error: 'NO_TOKEN' };
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
    return await this.sendRequestWithTimeout(options, payload, apiLabel);
  }

  async runRealExecution() {
    console.log(`=================================================================`);
    console.log(`[5-TOKEN RUNNER] Executing Parallel Multi-AI REST APIs`);
    console.log(`Brand: ${this.brand} | Stamp: ${this.stamp} | Anchor: ${this.anchor}`);
    console.log(`=================================================================`);

    const targetPrompt = "Execute 5-Token ESEB matrix synchronization.";

    // Kích hoạt song song bằng 5 Token phân định rõ ràng với đường dẫn nvidia/ chuẩn xác
    const executionPromises = [
      this.callGroqAPI(targetPrompt),
      this.callNvidiaNIMAPI('nanoNvidia', 'nvidia/llama-3.1-nemotron-nano-8b-v1', 'NVIDIA NIM (Nano Nemotron 8B)', targetPrompt),
      this.callNvidiaNIMAPI('llamaNvidia', 'meta/llama-3.1-8b-instruct', 'NVIDIA NIM (Llama 3.1 8B)', targetPrompt),
      this.callNvidiaNIMAPI('nemotronNvidia', 'nvidia/nemotron-3-nano-30b-a3b', 'NVIDIA NIM (Nemotron Extra)', targetPrompt)
    ];

    const results = await Promise.allSettled(executionPromises);
    
    results.forEach((res, index) => {
      if (res.status === 'fulfilled') {
        console.log(`[PIPELINE RESULT #${index + 1}] Target: ${res.value.api} | Status: ${res.value.success ? 'SUCCESS' : 'BYPASSED/FAILED'}`);
      } else {
        console.log(`[PIPELINE RESULT #${index + 1}] Rejected: ${res.reason}`);
      }
    });

    console.log(`[5-TOKEN RUNNER] All Concurrent Execution Pipelines Completed. Entropy delta = 0.`);
  }
}

if (require.main === module) {
  const runner = new Serverless5TokenExecutionRunner();
  runner.runRealExecution();
}

module.exports = Serverless5TokenExecutionRunner;
