/* ==========================================================================
   ESEB SERVERLESS RUNNER ENGINE (ULTRASOTA PSEO GEO LLMS)
   MODULE: Protocols/Ultrasota_Pseo_Geo_Llms.js
   STAMP: V-STAMP-24 | ¢24 ANCHOR | DYNAMIC FILE DISCOVERY SITEMAP ENGINE
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

  // Bóc tách Domain động từ CNAME hoặc GITHUB_REPOSITORY
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

  // TỰ ĐỘNG QUÉT CÂY THƯ MỤC ĐỂ PHÁT HIỆN TOÀN BỘ FILE .HTML THỰC TẾ
  scanHtmlFiles(dirPath = '.', fileList = []) {
    const files = fs.readdirSync(dirPath);

    files.forEach(file => {
      // Bỏ qua thư mục ẩn và node_modules
      if (file.startsWith('.') || file === 'node_modules') return;

      const filePath = path.join(dirPath, file);
      const stat = fs.statSync(filePath);

      if (stat.isDirectory()) {
        this.scanHtmlFiles(filePath, fileList);
      } else if (file.endsWith('.html')) {
        // Chuẩn hóa đường dẫn tương đối
        let relativePath = filePath.replace(/\\/g, '/');
        if (relativePath.startsWith('./')) relativePath = relativePath.substring(2);
        fileList.push(relativePath);
      }
    });

    return fileList;
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
    console.log(`[ULTRASOTA RUNNER] Executing Dynamic Identity & File Discovery Engine`);
    console.log(`Target Domain: ${targetDomain} | Stamp: ${this.stamp}`);
    console.log(`=================================================================`);

    await this.generateDynamicSitemapFromDiscovery(targetDomain);
    
    console.log(`[ULTRASOTA RUNNER] Execution Completed. Dynamic Discovery Sitemap Ready.`);
    process.exit(0);
  }
}

if (require.main === module) {
  new UltrasotaPseoGeoLlmsRunner().runRealExecution();
}

module.exports = UltrasotaPseoGeoLlmsRunner;
