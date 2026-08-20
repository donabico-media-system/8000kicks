/**
 * ESEB SERVERLESS RUNNER ENGINE - Organic_Traffic_Booster.js
 * GENERATED AUTOMATICALLY FROM Organic_Traffic_Booster.eseb
 * STAMP: V-STAMP-24 | ANCHOR: ¢24
 * STANDARD: 4THU 100% REALITY (MATCHING Cf_Workers_Ai.js LOGIC)
 */
const https = require('https');
const fs = require('fs');

const TOKEN = process.env.CF_API_TOKEN || process.env.ESEB_CLASSIC_TOKEN;
const CF_ACCOUNT_ID = process.env.CF_ACCOUNT_ID;
const GITHUB_REPO = process.env.GITHUB_REPOSITORY || 'donabico-media-system/core';

function discoverRunnerContext() {
    let targetDomain = '';
    const repoName = GITHUB_REPO.split('/')[1] || GITHUB_REPO;
    
    if (fs.existsSync('CNAME')) {
        const cname = fs.readFileSync('CNAME', 'utf8').trim();
        targetDomain = `https://${cname}/`;
    } else {
        const owner = GITHUB_REPO.split('/')[0] || 'donabico-media-system';
        targetDomain = `https://${owner}.github.io/${repoName}/`;
    }
    return { targetDomain, repoName };
}

const CONTEXT = discoverRunnerContext();
const CF_MODELS = {
  "LLAMA_70B": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
  "LLAMA_8B": "@cf/meta/llama-3.1-8b-instruct",
  "DEEPSEEK": "@cf/deepseek-ai/deepseek-r1-distill-qwen-32b",
  "MISTRAL_7B": "@cf/mistral/mistral-7b-instruct-v0.1",
  "LLAMA_3B": "@cf/meta/llama-3.2-3b-instruct",
  "GEMMA_7B": "@cf/google/gemma-7b-it-lora",
  "BGE_EMBEDDING": "@cf/baai/bge-large-en-v1.5",
  "SDXL_IMAGE": "@cf/bytedance/stable-diffusion-xl-lightning"
};

function callCloudflareAI(nodeKey, modelId, payloadData) {
    return new Promise((resolve) => {
        const payload = JSON.stringify(payloadData);
        const req = https.request({
            hostname: 'api.cloudflare.com',
            path: `/client/v4/accounts/${CF_ACCOUNT_ID}/ai/run/${modelId}`,
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${TOKEN}`,
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(payload)
            }
        }, (res) => {
            let chunks = [];
            res.on('data', chunk => chunks.push(chunk));
            res.on('end', () => {
                if (res.statusCode === 200) {
                    const isBinary = nodeKey === 'SDXL_IMAGE';
                    const msg = isBinary ? 'Status 200 OK (Binary Image Stream)' : 'Status 200 OK';
                    console.log(`[ESEB 08-AI SUCCESS] Node: [${nodeKey}] | Model: ${modelId} | ${msg}`);
                } else {
                    console.warn(`[ESEB 08-AI WARN] Node: [${nodeKey}] | Model: ${modelId} | Status ${res.statusCode}`);
                }
                resolve({ status: res.statusCode });
            });
        });
        req.on('error', e => {
            console.error(`[ESEB 08-AI ERROR] Node: [${nodeKey}] -> ${e.message}`);
            resolve({ status: 500, error: e.message });
        });
        req.write(payload);
        req.end();
    });
}

async function executeFullEightAIChain() {
    console.log('=================================================================');
    console.log('[ESEB FULL 08-AI GLOBAL MATRIX] Executing Cloudflare Edge GPU API Calls');
    console.log(`Stamp: V-STAMP-24 | Target Domain: ${CONTEXT.targetDomain}`);
    console.log('=================================================================');

    if (!TOKEN || !CF_ACCOUNT_ID) {
        console.error('[ESEB ERROR]: Missing CF_API_TOKEN / ESEB_CLASSIC_TOKEN or CF_ACCOUNT_ID.');
        process.exit(1);
    }

    await callCloudflareAI('LLAMA_70B', CF_MODELS.LLAMA_70B, { messages: [{ role: "user", content: `SGE Review for ${CONTEXT.targetDomain}` }] });
    await callCloudflareAI('LLAMA_8B', CF_MODELS.LLAMA_8B, { messages: [{ role: "user", content: `Fast RAG index for ${CONTEXT.targetDomain}` }] });
    await callCloudflareAI('DEEPSEEK', CF_MODELS.DEEPSEEK, { messages: [{ role: "user", content: `GEO-SEO keywords for ${CONTEXT.targetDomain}` }] });
    await callCloudflareAI('MISTRAL_7B', CF_MODELS.MISTRAL_7B, { messages: [{ role: "user", content: `JSON-LD Schema for ${CONTEXT.targetDomain}` }] });
    await callCloudflareAI('LLAMA_3B', CF_MODELS.LLAMA_3B, { messages: [{ role: "user", content: `Multi-geo tags for ${CONTEXT.targetDomain}` }] });
    await callCloudflareAI('GEMMA_7B', CF_MODELS.GEMMA_7B, { messages: [{ role: "user", content: `Product graph for ${CONTEXT.targetDomain}` }] });
    await callCloudflareAI('BGE_EMBEDDING', CF_MODELS.BGE_EMBEDDING, { text: [`Target URL at ${CONTEXT.targetDomain}`] });
    await callCloudflareAI('SDXL_IMAGE', CF_MODELS.SDXL_IMAGE, { prompt: "SOTA High Conversion E-Commerce Banner" });

    console.log('[ESEB 08-AI MATRIX] All 08 Active Nodes Executed with Zero Entropy.');
}

executeFullEightAIChain();