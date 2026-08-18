// ESEB SERVERLESS RUNNER ENGINE - CLOUDFLARE EDGE AI & INDEXNOW BROADCAST
const CF_ACCOUNT_ID = process.env.CF_ACCOUNT_ID;
const CF_API_TOKEN = process.env.CF_API_TOKEN;

if (!CF_ACCOUNT_ID || !CF_API_TOKEN) {
    console.error("[ESEB_RUNNER_ERROR] Missing CF_ACCOUNT_ID or CF_API_TOKEN in Environment Variables.");
    process.exit(1);
}

const CF_MATRIX_NODES = [
    { key: "MISTRAL_7B", model: "@cf/mistral/mistral-7b-instruct-v0.1", body: { messages: [{ role: "user", content: "Validate product snippet rating and review schema." }] } }
];

async function executeRunner() {
    const node = CF_MATRIX_NODES[0];
    const url = `https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/ai/run/${node.model}`;
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${CF_API_TOKEN}`, 'Content-Type': 'application/json' },
            body: JSON.stringify(node.body)
        });
        console.log(`[CF_EDGE_NODE] Node: ${node.key} | Status: ${response.status} ${response.statusText}`);
    } catch (err) {
        console.error(`[NODE_FATAL] Error: ${err.message}`);
    }
}

executeRunner();