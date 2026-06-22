// .github/scripts/push-to-google-ads.js
// EATHESEN V3000-Ω | Real Google Ads API Push (PMax)
// Phiên bản đã sửa lỗi: Tự chứa payload, không cần file payload.json

require('dotenv').config();
const { GoogleAdsApi } = require('google-ads-api');

const client = new GoogleAdsApi({
  client_id: process.env.GOOGLE_ADS_CLIENT_ID,
  client_secret: process.env.GOOGLE_ADS_CLIENT_SECRET,
  developer_token: process.env.GOOGLE_ADS_DEVELOPER_TOKEN,
});

// ==================== PAYLOAD ĐÃ NHÚNG SẴN (từ index.html) ====================
const payload = {
  campaign_name: "8000Kicks_Waterproof_Hemp_Shoes_PMax_HyperMax_2026",
  asset_group_name: "SuperCore_Main_Asset_Group",
  final_url: "https://8000kicks.sjv.io/donabico_global_media",
  headlines: [
    { text: "8000Kicks — Giày Gai Dầu Chống Nước Thật Sự | Bio-Shield Plant-Based" },
    { text: "Giày Hemp Bền Vững Carbon Negative | Ethical Footwear 2026" },
    { text: "Travel Shoes Siêu Nhẹ Gấp Gọn Chống Nước | PMax + Hyper Q Optimized" },
    { text: "Hơn 50.000 Khách Hàng Tin Dùng | Limited Stock - ROI Max" },
    { text: "Chỉ 320g/Chiếc — Thay Thế 3 Đôi Giày Trong Vali | All-Weather" }
  ],
  descriptions: [
    { text: "Công nghệ Bio-Shield Plant-Based giữ chân khô ráo trong mưa, bùn, biển. Hemp tự nhiên, bền gấp 3 lần, carbon negative." },
    { text: "Algae Bloom Insole + Hemp Canvas. Eco-friendly, vegan, ethical. Target ROAS 450%+ | Hyper Max Q-Learning" },
    { text: "Phù hợp du lịch, hiking, đi mưa. Lightweight, packable, all-weather. SEO Automatic + ADS Automatic 24/7" }
  ],
  images: [
    { url: "https://www.8000kicks.com/cdn/shop/files/8000Kicks_147_375x250_crop_center.jpg", type: "LANDSCAPE" },
    { url: "https://www.8000kicks.com/cdn/shop/files/8000Kicks_175_375x250_crop_center.jpg", type: "SQUARE" }
  ],
  call_to_action: "SHOP_NOW",
  target_roas: 4.8,
  bidding_strategy: "MAXIMIZE_CONVERSION_VALUE",
  audience_signals: ["eco_conscious_travelers", "sustainable_fashion", "outdoor_adventurers", "waterproof_shoes_buyers"],
  conversion_tracking: {
    gtag_event: "purchase",
    conversion_id: "AW-YOUR_CONVERSION_ID",
    conversion_label: "YOUR_LABEL"
  },
  keywords: ["giày chống nước", "hemp shoes", "waterproof travel shoes", "sustainable footwear", "eco friendly sneakers", "giày gai dầu"]
};

// ==================== HÀM PUSH THẬT ====================
async function pushToGoogleAds(payloadData) {
  const customer = client.Customer({
    customer_id: process.env.GOOGLE_ADS_CUSTOMER_ID,
    refresh_token: process.env.GOOGLE_ADS_REFRESH_TOKEN,
  });

  console.log(`[REAL PUSH] Bắt đầu push cho campaign: ${payloadData.campaign_name}`);

  try {
    // TODO: Mở rộng logic mutate thật theo Google Ads API docs cho PMax
    // Hiện tại: Log + chuẩn bị operations (bạn có thể thêm mutate thực tế sau)

    console.log("[REAL PUSH] Payload đã nhận:", {
      campaign: payloadData.campaign_name,
      headlines: payloadData.headlines.length,
      descriptions: payloadData.descriptions.length,
      images: payloadData.images.length
    });

    // Ví dụ log để kiểm tra
    console.log("✅ Script chạy thành công. Sẵn sàng mutate operations.");

    // Nếu muốn test thật, uncomment và hoàn thiện phần mutate theo docs:
    // const response = await customer.mutate([...operations]);
    // console.log("Google Ads response:", response);

    return {
      status: "SUCCESS",
      campaign: payloadData.campaign_name,
      timestamp: new Date().toISOString(),
      message: "Payload đã được xử lý. Thêm logic mutate để push thật."
    };

  } catch (error) {
    console.error("❌ Lỗi khi push Google Ads:", error);
    throw error;
  }
}

// ==================== CHẠY KHI GỌI TRỰC TIẾP ====================
if (require.main === module) {
  console.log("🚀 Chạy push-to-google-ads.js (embedded payload)");
  pushToGoogleAds(payload).catch(console.error);
}

module.exports = { pushToGoogleAds, payload };
