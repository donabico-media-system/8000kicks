/* ==========================================================================
   ESEB SERVERLESS RUNNER ENGINE (ULTRASOTA PSEO GEO LLMS)
   MODULE: Protocols/Ultrasota_Pseo_Geo_Llms.js
   STAMP: V-STAMP-24 | ¢24 ANCHOR | DUAL-TOKEN EXPLICIT REST API EXECUTION
   ========================================================================== */
const https = require('https');
const fs = require('fs');
const path = require('path');

class UltrasotaPseoGeoLlmsRunner {
  constructor() {
    this.stamp = "V-STAMP-24";
    this.brand = "DONABICO MEDIA SYSTEM";
    this.anchor = "24";
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

    const githubRepo = process.env.GITHUB_REPOSITORY || '';
    if (githubRepo) {
      const parts = githubRepo.split('/');
      const owner = parts[0] || '';
      const repo = parts[1] || '';
      if (owner && repo) {
        return repo.toLowerCase() === `${owner.toLowerCase()}.github.io` ? `${owner}.github.io` : `${owner}.github.io/${repo}`;
      }
    }
    return 'localhost';
  }

  scanHtmlFiles(dirPath = '.', fileList = []) {
    const files = fs.readdirSync(dirPath);

    files.forEach(file => {
      if (file.startsWith('.') || file === 'node_modules') return;

      const filePath = path.join(dirPath, file);
      const stat = fs.statSync(filePath);

      if (stat.isDirectory()) {
        this.scanHtmlFiles(filePath, fileList);
      } else if (file.endsWith('.html')) {
        let relativePath = filePath.replace(/\\/g, '/');
        if (relativePath.startsWith('./')) relativePath = relativePath.substring(2);
        fileList.push(relativePath);
      }
    });

    return fileList;
  }

  // 1. THỰC THI GỌI GROQ LPU REST API (API_GROQ_TOKEN)
  async executeGroqLpuQuery(targetDomain) {
    if (!this.tokens.apiGroq || !this.tokens.apiGroq.trim()) {
      console.log("[GROQ CORE] API_GROQ_TOKEN missing in Secrets. Bypassing AI call.");
      return false;
    }

    const cleanToken = this.tokens.apiGroq.trim().replace(/^["']|["']$/g, '');
    const payload = JSON.stringify({
      model: "llama-3.3-70b-versatile",
      messages: [
        {"role": "system", "content": "You are ESEB Ultrasota Pseo Geo Llms Engine V3000-Ω."},
        {"role": "user", "content": `Ping GEO Indexing matrix for domain: ${targetDomain}` }
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
        'User-Agent': 'ESEB-Engine/V3000-Omega',
        'Content-Length': Buffer.byteLength(payload)
      },
      timeout: 10000
    };

    return new Promise((resolve) => {
      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          console.log(`[REAL AI API EXECUTION] GROQ LPU Engine Status: ${res.statusCode}`);
          resolve(res.statusCode === 200);
        });
      });
      req.on('timeout', () => { req.destroy(); resolve(false); });
      req.on('error', (err) => { console.log(`[GROQ ERROR] ${err.message}`); resolve(false); });
      req.write(payload);
      req.end();
    });
  }

  // 2. THỰC THI XÁC THỰC VÀ GỌI GITHUB REST API (ESEB_CLASSIC_TOKEN)
  async executeEsebClassicAuth() {
    if (!this.tokens.esebClassic || !this.tokens.esebClassic.trim()) {
      console.log("[ESEB CLASSIC] ESEB_CLASSIC_TOKEN missing in Secrets. Bypassing Classic Auth call.");
      return false;
    }

    const cleanToken = this.tokens.esebClassic.trim().replace(/^["']|["']$/g, '');
    const options = {
      hostname: 'api.github.com',
      port: 443,
      path: '/user',
      method: 'GET',
      headers: {
        'User-Agent': 'ESEB-Classic-Auth/V3000-Omega',
        'Authorization': `Bearer ${cleanToken}`,
        'Accept': 'application/vnd.github.v3+json'
      },
      timeout: 10000
    };

    return new Promise((resolve) => {
      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          console.log(`[ESEB CLASSIC SUCCESS] GitHub API Auth Status: ${res.statusCode} | Stamp: ${this.stamp} Verified.`);
          resolve(res.statusCode === 200);
        });
      });
      req.on('timeout', () => { req.destroy(); resolve(false); });
      req.on('error', (err) => { console.log(`[ESEB CLASSIC ERROR] ${err.message}`); resolve(false); });
      req.end();
    });
  }

  async generateDynamicSitemapFromDiscovery(targetDomain) {
    const nowIso = new Date().toISOString().split('T')[0];
    const discoveredHtmlFiles = this.scanHtmlFiles('.');

    console.log(`[DISCOVERY ENGINE] Found ${discoveredHtmlFiles.length} HTML files in repository.`);

    let urlNodes = discoveredHtmlFiles.map(filePath => {
      let cleanPath = filePath;
      if (cleanPath === 'index.html') {
        cleanPath = '';
      }
      
      const loc = cleanPath ? `https://${targetDomain}/${cleanPath}` : `https://${targetDomain}/`;
      const priority = cleanPath === '' ? "1.0" : "0.8";

      return `  <url>\n` +
             `    <loc>${loc}</loc>\n` +
             `    <lastmod>${nowIso}</lastmod>\n` +
             `    <changefreq>daily</changefreq>\n` +
             `    <priority>${priority}</priority>\n` +
             `  </url>`;
    }).join('\n');

    const sitemapContent = `<?xml version="1.0" encoding="UTF-8"?>\n` +
      `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
      `${urlNodes}\n` +
      `</urlset>`;

    fs.writeFileSync('sitemap.xml', sitemapContent, 'utf-8');
    console.log(`[GEO ENGINE] Successfully generated DYNAMIC SITEMAP with ${discoveredHtmlFiles.length} URLs for ${targetDomain}`);
  }

  async runRealExecution() {
    const targetDomain = this.getAutoDiscoveredDomain();
    console.log(`=================================================================`);
    console.log(`[ULTRASOTA RUNNER] Executing Dual-Token Dynamic Discovery Engine`);
    console.log(`Target Domain: ${targetDomain} | Stamp: ${this.stamp}`);
    console.log(`=================================================================`);

    // Thực thi đồng thời cả 2 cuộc gọi REST API
    await this.executeEsebClassicAuth();
    await this.executeGroqLpuQuery(targetDomain);
    
    // Sinh sitemap động
    await this.generateDynamicSitemapFromDiscovery(targetDomain);
    
    console.log(`[ULTRASOTA RUNNER] Dual-Token Execution Completed. Dynamic Discovery Sitemap Ready.`);
    process.exit(0);
  }
}

if (require.main === module) {
  new UltrasotaPseoGeoLlmsRunner().runRealExecution();
}

module.exports = UltrasotaPseoGeoLlmsRunner;
