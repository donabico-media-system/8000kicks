// ESEB SERVERLESS RUNNER ENGINE - FULL 08 CLOUDFLARE EDGE GPU AI MATRIX PARALLEL EXECUTION
const CF_ACCOUNT_ID = process.env.CF_ACCOUNT_ID;
const CF_API_TOKEN = process.env.CF_API_TOKEN;

if (!CF_ACCOUNT_ID || !CF_API_TOKEN) {
    console.error("[ESEB_RUNNER_ERROR] Missing CF_ACCOUNT_ID or CF_API_TOKEN in Environment Variables.");
    process.exit(1);
}

// 08 Cloudflare Edge GPU AI Matrix Registry
const CF_MATRIX_NODES = [
    { key: "LLAMA_70B", model: "@cf/meta/llama-3.3-70b-instruct-fp8-fast", type: "chat", body: { messages: [{ role: "user", content: "Generate affiliate review summary." }] } },
    { key: "LLAMA_8B", model: "@cf/meta/llama-3.1-8b-instruct", type: "chat", body: { messages: [{ role: "user", content: "Rapid query fallback test." }] } },
    { key: "DEEPSEEK", model: "@cf/deepseek-ai/deepseek-r1-distill-qwen-32b", type: "chat", body: { messages: [{ role: "user", content: "GEO-SEO optimization reasoning." }] } },
    { key: "MISTRAL_7B", model: "@cf/mistral/mistral-7b-instruct-v0.1", type: "chat", body: { messages: [{ role: "user", content: "JSON-LD schema validation." }] } },
    { key: "LLAMA_3B", model: "@cf/meta/llama-3.2-3b-instruct", type: "chat", body: { messages: [{ role: "user", content: "Fast edge localization." }] } },
    { key: "GEMMA_7B", model: "@cf/google/gemma-7b-it-lora", type: "chat", body: { messages: [{ role: "user", content: "Context enrichment for e-commerce." }] } },
    { key: "BGE_EMBEDDING", model: "@cf/baai/bge-large-en-v1.5", type: "embedding", body: { text: ["8000kicks waterproof hemp shoes eco-friendly"] } },
    { key: "SDXL_IMAGE", model: "@cf/bytedance/stable-diffusion-xl-lightning", type: "image", body: { prompt: "eco-friendly waterproof hemp sneakers product banner" } }
];

async function callCloudflareNode(node) {
    const url = `https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/ai/run/${node.model}`;
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${CF_API_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(node.body)
        });

        console.log(`[CF_EDGE_NODE] Node: ${node.key} | Model: ${node.model} | Status: ${response.status} ${response.statusText}`);
        
        if (response.status === 200) {
            return { node: node.key, status: 200, ok: true };
        } else {
            const errText = await response.text();
            console.error(`[NODE_ERROR] ${node.key} failed with Status ${response.status}: ${errText}`);
            return { node: node.key, status: response.status, ok: false };
        }
    } catch (err) {
        console.error(`[NODE_FATAL] ${node.key} request error: ${err.message}`);
        return { node: node.key, status: 500, ok: false, error: err.message };
    }
}

async function executeFullMatrix() {
    console.log("==================================================================");
    console.log("[ESEB_RUNNER] STARTING FULL 08 CLOUDFLARE EDGE GPU AI MATRIX EXECUTION");
    console.log("==================================================================");

    const results = await Promise.allSettled(CF_MATRIX_NODES.map(node => callCloudflareNode(node)));
    
    let successCount = 0;
    results.forEach((res) => {
        if (res.status === 'fulfilled' && res.value.ok) {
            successCount++;
        }
    });

    console.log("==================================================================");
    console.log(`[ESEB_RUNNER_SUMMARY] Matrix Execution Finished: ${successCount}/8 Nodes Responded 200 OK.`);
    console.log("==================================================================");

    if (successCount === 0) {
        process.exit(1);
    }
}

executeFullMatrix();