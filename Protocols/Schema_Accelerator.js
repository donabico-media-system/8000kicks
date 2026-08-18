// ESEB SERVERLESS RUNNER ENGINE - CLOUDFLARE 08 EDGE GPU AI MATRIX
const https = require('https');

const CF_ACCOUNT_ID = process.env.CF_ACCOUNT_ID;
const CF_API_TOKEN = process.env.CF_API_TOKEN;
const ESEB_CLASSIC_TOKEN = process.env.ESEB_CLASSIC_TOKEN;

if (!CF_ACCOUNT_ID || !CF_API_TOKEN) {
    console.error("[ESEB_RUNNER_ERROR] Missing CF_ACCOUNT_ID or CF_API_TOKEN in Secrets.");
    process.exit(1);
}

// 08 Cloudflare Edge GPU AI Matrix Registry
const CF_MODELS = {
    LLAMA_70B: "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
    LLAMA_8B: "@cf/meta/llama-3.1-8b-instruct",
    DEEPSEEK: "@cf/deepseek-ai/deepseek-r1-distill-qwen-32b",
    MISTRAL_7B: "@cf/mistral/mistral-7b-instruct-v0.1",
    LLAMA_3B: "@cf/meta/llama-3.2-3b-instruct",
    GEMMA_7B: "@cf/google/gemma-7b-it-lora",
    BGE_EMBEDDING: "@cf/baai/bge-large-en-v1.5",
    SDXL_IMAGE: "@cf/bytedance/stable-diffusion-xl-lightning"
};

// Gọi mặc định Node MISTRAL_7B tối ưu JSON-LD Schema
const targetModel = CF_MODELS.MISTRAL_7B;

const payload = JSON.stringify({
    messages: [
        { role: "system", content: "You are ESEB Schema Optimizer. Generate clean W3C JSON-LD Product Schema." },
        { role: "user", content: "Verify 8000kicks Merchant Listing Schema for GSC." }
    ]
});

const options = {
    hostname: 'api.cloudflare.com',
    path: `/client/v4/accounts/${CF_ACCOUNT_ID}/ai/run/${targetModel}`,
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${CF_API_TOKEN}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
    }
};

const req = https.request(options, (res) => {
    console.log(`[CLOUDFLARE_EDGE_AI_EXECUTION] Model: ${targetModel} | Status: ${res.statusCode}`);
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        if (res.statusCode === 200) {
            console.log("[ESEB_RUNNER_SUCCESS] Cloudflare AI Real REST Response Received (Status 200).");
        }
    });
});

req.on('error', (e) => { console.error(`[CLOUDFLARE_API_ERROR] ${e.message}`); });
req.write(payload);
req.end();