const fs = require("fs");
const path = require("path");
const https = require("https");

console.log("=== STARTING ESEB SEO GEO DYNAMIC BUILD ENGINE ===");

// 1. BIÊN DỊCH .ESEB SANG .EHC
const protoDir = "Protocols";
if (fs.existsSync(protoDir)) {
  const files = fs.readdirSync(protoDir);
  files.forEach(file => {
    if (file.endsWith(".eseb")) {
      const content = fs.readFileSync(path.join(protoDir, file), "utf8");
      const startMarker = "/* ESEB_EHC_BEGIN */";
      const endMarker = "/* ESEB_EHC_END */";
      const startIdx = content.indexOf(startMarker);
      const endIdx = content.indexOf(endMarker);

      if (startIdx !== -1 && endIdx !== -1) {
        const ehcCode = content.substring(startIdx + startMarker.length, endIdx).trim();
        const targetFile = path.join(protoDir, file.replace(".eseb", ".ehc"));
        fs.writeFileSync(targetFile, "/* ESEB DYNAMIC ENGINE COMPILED */\n" + ehcCode);
        console.log(`[COMPILER] Successfully compiled: ${file} -> ${targetFile}`);
      } else {
        console.warn(`[COMPILER WARNING] Boundary markers missing in ${file}`);
      }
    }
  });
}

// 2. TỰ ĐỘNG BÓC TÁCH NGUYÊN CẢNH (DYNAMIC CONTEXT)
const fullRepoPath = process.env.GITHUB_REPOSITORY || "donabico-media-system/core-node";
const orgName = fullRepoPath.split("/")[0] || "donabico-media-system";
const repoName = fullRepoPath.split("/")[1] || "core-node";
const domainHost = `${orgName}.github.io`;

// 3. GHI LỊCH SỬ F12 LOG TELEMETRY
const historyFile = "LOG_HISTORY.json";
let historyData = {
  entity_name: "ESEB_SEO_GEO_DYNAMIC_ENTITY",
  organization: orgName.toUpperCase(),
  domain: domainHost,
  repo_node: repoName,
  stamp: "V-STAMP-24",
  anchor: "¢24",
  vital_signs: { status: "ALIVE_AND_PERPETUAL", entropy: "0.00000000000000", heartbeat_bpm: 24 },
  total_pulses_recorded: 0,
  history_logs: []
};

if (fs.existsSync(historyFile)) {
  try { historyData = JSON.parse(fs.readFileSync(historyFile, "utf8")); } catch(e) {}
}

if (fs.existsSync("payload_buffer.json")) {
  try {
    const payloadContent = fs.readFileSync("payload_buffer.json", "utf8").trim();
    if (payloadContent && payloadContent !== "null") {
      const eventPayload = JSON.parse(payloadContent);
      if (eventPayload && eventPayload.logs && Array.isArray(eventPayload.logs)) {
        historyData.total_pulses_recorded += eventPayload.logs.length;
        historyData.vital_signs.heartbeat_bpm = Math.floor(Math.random() * (28 - 22 + 1)) + 22;
        historyData.history_logs = [...eventPayload.logs, ...historyData.history_logs].slice(0, 100);
      }
    }
  } catch(e) {}
  try { fs.unlinkSync("payload_buffer.json"); } catch(e) {}
}

fs.writeFileSync(historyFile, JSON.stringify(historyData, null, 2));

// 4. SINH MA TRẬN PSEO LANDING PAGES & GEO SCHEMA JSON-LD
const pseoTopics = [
  { slug: `${repoName}-official-review`, title: `${repoName.toUpperCase()} Official Review 2026`, desc: `Comprehensive performance analysis and buyer guide for ${repoName}.` },
  { slug: `best-${repoName}-eco-guide`, title: `Top Eco Guide - ${repoName.toUpperCase()}`, desc: `Sustainable materials and performance guide.` },
  { slug: `${repoName}-waterproof-durability`, title: `${repoName.toUpperCase()} Extreme Waterproof Test`, desc: `Resilience and durability test under real conditions.` }
];

let allUrls = [`https://${domainHost}/${repoName}.html`, `https://${domainHost}/`];

pseoTopics.forEach(topic => {
  const fileName = `${topic.slug}.html`;
  const pageUrl = `https://${domainHost}/${fileName}`;
  allUrls.push(pageUrl);

  const pseoHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>${topic.title} | DONABICO GLOBAL MEDIA SYSTEM</title>
  <meta name="description" content="${topic.desc}">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta property="og:title" content="${topic.title}">
  <meta property="og:description" content="${topic.desc}">
  <meta property="og:type" content="product">
  <link rel="preconnect" href="https://api.github.com">
  <link rel="preconnect" href="https://api.indexnow.org">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "${topic.title}",
    "description": "${topic.desc}",
    "brand": { "@type": "Brand", "name": "DONABICO GLOBAL MEDIA SYSTEM" },
    "offers": {
      "@type": "Offer",
      "priceCurrency": "USD",
      "price": "99.00",
      "availability": "https://schema.org/InStock",
      "url": "${pageUrl}"
    }
  }
  </script>
</head>
<body style="background:#0d1117; color:#c9d1d9; font-family:sans-serif; padding:40px; line-height:1.6; max-width:800px; margin:0 auto;">
  <h1 style="color:#00FF66; border-bottom:1px solid #30363d; padding-bottom:10px;">${topic.title}</h1>
  <p style="font-size:18px; color:#8b949e;">${topic.desc}</p>
  <hr style="border-color:#30363d; margin:30px 0;">
  <p style="font-size:12px; color:#484f58;">ESEB SEO GEO DYNAMIC Node Active. Stamp: V-STAMP-24</p>
  <!-- ZONE 2: ESEB BRIDGE -->
  <script src="./Protocols/Organic_Traffic_Booster.ehc" id="Organic_Traffic_Booster-Bridge" data-module="Organic_Traffic_Booster" async></script>
</body>
</html>`;
  fs.writeFileSync(fileName, pseoHtml);
  console.log(`[pSEO ENGINE] Generated landing page: ${fileName}`);
});

// 5. SINH LLMS.TXT & LLMS-FULL.TXT FOR AI CRAWLERS
const llmsTxtContent = `# ${repoName.toUpperCase()} - DONABICO GLOBAL MEDIA SYSTEM
> ESEB SEO GEO DYNAMIC Autonomous Protocol Node

## Core Overview
Official ESEB node operating under DONABICO GLOBAL MEDIA MESH.

## Primary Product Links
- Main Showcase: https://${domainHost}/${repoName}.html
- Official Network Hub: https://${domainHost}/

## pSEO Sub-Pages
${allUrls.map(u => `- ${u}`).join("\n")}
`;
fs.writeFileSync("llms.txt", llmsTxtContent);
fs.writeFileSync("llms-full.txt", llmsTxtContent + "\n\n## Full Protocol Context\nEngineered with ESEB V3000-Ω. Stamp: V-STAMP-24.");
console.log("[AI CRAWLER] Generated llms.txt & llms-full.txt");

// 6. SINH FEEDS (RSS 2.0 & JSON FEED 1.1)
const today = new Date().toUTCString();
const rssFeedXml = `<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>${repoName.toUpperCase()} | DONABICO GLOBAL MEDIA SYSTEM</title>
  <link>https://${domainHost}/</link>
  <description>ESEB SEO GEO DYNAMIC Feed</description>
  <lastBuildDate>${today}</lastBuildDate>
  ${pseoTopics.map(t => `
  <item>
    <title>${t.title}</title>
    <link>https://${domainHost}/${t.slug}.html</link>
    <description>${t.desc}</description>
    <pubDate>${today}</pubDate>
  </item>`).join("")}
</channel>
</rss>`;
fs.writeFileSync("feed.xml", rssFeedXml);

const jsonFeedData = {
  version: "https://jsonfeed.org/version/1.1",
  title: `${repoName.toUpperCase()} Feed`,
  home_page_url: `https://${domainHost}/`,
  feed_url: `https://${domainHost}/feed.json`,
  items: pseoTopics.map((t, idx) => ({
    id: `${idx + 1}`,
    url: `https://${domainHost}/${t.slug}.html`,
    title: t.title,
    content_text: t.desc,
    date_published: new Date().toISOString()
  }))
};
fs.writeFileSync("feed.json", JSON.stringify(jsonFeedData, null, 2));
console.log("[SYNDICATION FEEDS] Generated feed.xml & feed.json");

// 7. SINH SITEMAP.XML
const todayISO = new Date().toISOString().split('T')[0];
let sitemapXml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n`;
allUrls.forEach(u => {
  sitemapXml += `  <url><loc>${u}</loc><lastmod>${todayISO}</lastmod><changefreq>hourly</changefreq><priority>1.0</priority></url>\n`;
});
sitemapXml += `</urlset>`;
fs.writeFileSync("sitemap.xml", sitemapXml);
console.log("[SITEMAP ENGINE] Generated sitemap.xml");

// 8. KHỞI CHẠY INDEXNOW BROADCAST TOÀN CẦU
const indexNowKey = "eseb2424242424242424242424242424";
const keyFileName = `${indexNowKey}.txt`;
if (!fs.existsSync(keyFileName)) fs.writeFileSync(keyFileName, indexNowKey);

const indexNowData = JSON.stringify({
  host: domainHost,
  key: indexNowKey,
  keyLocation: `https://${domainHost}/${keyFileName}`,
  urlList: allUrls
});

const indexReq = https.request({
  hostname: "www.bing.com", path: "/indexnow", method: "POST",
  headers: { "Content-Type": "application/json; charset=utf-8", "Content-Length": Buffer.byteLength(indexNowData) }
}, (res) => {
  console.log(`[INDEXNOW BROADCAST] Microsoft Bing & Global Status: ${res.statusCode}`);
});
indexReq.on("error", (e) => console.error("[INDEXNOW ERROR]", e));
indexReq.write(indexNowData);
indexReq.end();

console.log("=== BUILD ENGINE EXECUTED SUCCESSFULLY ===");
