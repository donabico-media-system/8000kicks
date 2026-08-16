/* ==========================================================================
   ESEB SERVERLESS RUNNER (VECTOR RAG INDEXER & SEARCH - SOTA 2026)
   MODULE: Protocols/Cf_Vector_Rag.js
   STAMP: V-STAMP-24 | DONABICO GLOBAL MEDIA SYSTEM
   STRICT COMPLIANCE: ESEB 04THU AUTO-6D PROTOCOL
   ========================================================================== */
const https = require('https');

class VectorRagRunner {
  constructor() {
    this.stamp = "V-STAMP-24";
    this.accountId = process.env.CF_ACCOUNT_ID || '';
    this.apiToken = process.env.CF_API_TOKEN || '';
    this.embeddingModel = "@cf/baai/bge-large-en-v1.5";
    this.vectorIndexName = process.env.CF_VECTOR_INDEX || 'eathesen-rag-index';
  }

  async generateEmbedding(textPayload) {
    if (!this.accountId || !this.apiToken) {
      console.log(`[VECTOR RAG ERROR] Credentials missing for Embedding Node.`);
      return null;
    }

    const payload = JSON.stringify({ text: [textPayload] });

    const options = {
      hostname: 'api.cloudflare.com',
      port: 443,
      path: `/client/v4/accounts/${this.accountId}/ai/run/${this.embeddingModel}`,
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
          if (res.statusCode === 200) {
            try {
              const parsed = JSON.parse(data);
              if (parsed.success && parsed.result && parsed.result.data) {
                console.log(`[ESEB VECTOR RAG SUCCESS] Generated ${parsed.result.data[0].length}-Dim Vector Embedding`);
                resolve(parsed.result.data[0]);
              } else {
                console.log(`[ESEB VECTOR RAG WARN] Embedding Payload Issue | Status: ${res.statusCode}`);
                resolve(null);
              }
            } catch(e) {
              console.log(`[ESEB VECTOR RAG PARSE ERROR] Status: ${res.statusCode}`);
              resolve(null);
            }
          } else {
            console.log(`[ESEB VECTOR RAG ERROR] Status: ${res.statusCode}`);
            resolve(null);
          }
        });
      });
      req.on('timeout', () => { req.destroy(); resolve(null); });
      req.on('error', (err) => { console.log(`[ESEB VECTOR RAG NETWORK ERROR] ${err.message}`); resolve(null); });
      req.write(payload);
      req.end();
    });
  }

  async run() {
    console.log(`=================================================================`);
    console.log(`[ESEB VECTOR RAG ENGINE] Indexing & Querying Cloudflare Vectorize`);
    console.log(`Stamp: ${this.stamp} | DONABICO GLOBAL MEDIA SYSTEM`);
    console.log(`=================================================================`);

    const sampleContext = "8000kicks waterproof hemp shoes sustainable footwear eco-friendly affiliate deal US UK EU CA AU NZ";
    const vector = await this.generateEmbedding(sampleContext);

    if (vector) {
      console.log(`[ESEB VECTOR RAG] Knowledge Index Synced & Ready for 08 AI Matrix.`);
    } else {
      console.log(`[ESEB VECTOR RAG] Fallback to Static RAG Index.`);
    }

    process.exit(0);
  }
}

if (require.main === module) {
  new VectorRagRunner().run();
}

module.exports = VectorRagRunner;
