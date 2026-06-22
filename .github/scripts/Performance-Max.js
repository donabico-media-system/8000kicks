/**
 * Performance-Max.js - V4.0-ULTIMA-MAX (ENGLISH ONLY)
 * EATHESEN V3000-Ω SOTA | English Lock Enforced
 */

class UltimatePerformanceMaxAgent {
    constructor(configuration = {}) {
        this.signature = "V3000-Ω-ULTIMA-DECENTRALIZED-NETWORK-MAX";
        this.webhookUrl = configuration.webhookUrl || null;
        this.version = "4.0-ULTIMA-MAX";

        // === EXPANDED STATE & ACTION SPACE ===
        this.states = [
            'NAV_LOW_ENGAGED', 'NAV_HIGH_ENGAGED', 'INTENT_CRITICAL_HOT',
            'ADS_INTENT_PROMO', 'ADS_INTENT_URGENCY', 'ADS_INTENT_QUALITY',
            'ANOMALY_THREAT', 'SWARM_CONSENSUS', 'CONVERSION_READY'
        ];
        this.actions = [
            'VARIANT_PROMO_AGGRESSIVE', 'VARIANT_URGENCY_SCARCITY', 'VARIANT_HYPER_SOCIAL_PROOF',
            'VARIANT_DYNAMIC_OFFER', 'VARIANT_SEO_AEO_PUSH', 'VARIANT_TRUST_MAX'
        ];

        this.alpha = 0.28;
        this.gamma = 0.92;
        this.epsilon = 0.25;
        this.epsilonDecay = 0.985;
        this.minEpsilon = 0.03;
        this.temperature = 1.2;

        this.storageKey = 'V3000_ULTIMA_MAX_NEURAL_MATRIX';
        this.qTable = this.synchronizeNeuralMatrix();
        this.experienceReplay = [];
        this.maxReplaySize = 128;

        this.adsContext = this.parseExternalAdsIntent();
        this.currentState = this.determineInitialState();

        this.activeActionIdx = 0;
        this.epochStartTime = performance.now();

        this.telemetry = {
            maxScrollDepth: 0,
            scrollVelocityMax: 0,
            ctaInteractionCount: 0,
            conversionStateReached: false,
            lastScrollPosition: 0,
            lastScrollTime: performance.now(),
            mouseDwellTime: 0,
            clickHeatmap: {},
            dwellTimeDistribution: []
        };

        this.signalHistory = [];
        this.swarmEnergy = 0.65;
        this.selfHealingCount = 0;

        this.igniteEngine();
    }

    parseExternalAdsIntent() {
        try {
            const urlParams = new URLSearchParams(window.location.search);
            const utmTerm = (urlParams.get('utm_term') || urlParams.get('q') || '').toLowerCase();
            const utmContent = (urlParams.get('utm_content') || '').toLowerCase();
            const utmCampaign = (urlParams.get('utm_campaign') || '').toLowerCase();
            
            const combinedContext = `${utmTerm} ${utmContent} ${utmCampaign}`;
            console.log(`%c[Performance-Max MAX INBOUND] Parsing External Ads Copy Context: "${combinedContext}"`, "color: #3498db; font-weight: bold;");

            if (combinedContext.match(/(khuyen mai|giam gia|uudai|promo|sale|voucher|price|discount)/g)) return 'PROMO';
            if (combinedContext.match(/(gioi han|con lai|doc quyen|sap het|urgency|limited|last|scarcity)/g)) return 'URGENCY';
            if (combinedContext.match(/(chinh hang|uy tin|chat luong|tot nhat|review|bền|chống nước|quality|trust|premium)/g)) return 'QUALITY';
            return 'GENERIC';
        } catch (e) {
            return 'GENERIC';
        }
    }

    determineInitialState() {
        switch (this.adsContext) {
            case 'PROMO': return 'ADS_INTENT_PROMO';
            case 'URGENCY': return 'ADS_INTENT_URGENCY';
            case 'QUALITY': return 'ADS_INTENT_QUALITY';
            default: return 'NAV_LOW_ENGAGED';
        }
    }

    synchronizeNeuralMatrix() {
        try {
            const centralMatrix = localStorage.getItem(this.storageKey);
            if (centralMatrix) return JSON.parse(centralMatrix);
            const pristineMatrix = {};
            this.states.forEach(s => pristineMatrix[s] = new Array(this.actions.length).fill(0.0000));
            return pristineMatrix;
        } catch (e) {
            this.selfHealingCount++;
            const fallback = {};
            this.states.forEach(s => fallback[s] = new Array(this.actions.length).fill(0.015));
            return fallback;
        }
    }

    persistNeuralMatrix() {
        try { localStorage.setItem(this.storageKey, JSON.stringify(this.qTable)); } catch (e) {}
    }

    stochasticActionSelection(state) {
        if (state.startsWith('ADS_INTENT_') && Math.random() > 0.04) {
            const actionScores = this.qTable[state];
            if (actionScores.every(v => v === 0)) {
                if (state === 'ADS_INTENT_PROMO') return 0;
                if (state === 'ADS_INTENT_URGENCY') return 1;
                if (state === 'ADS_INTENT_QUALITY') return 2;
            }
            return actionScores.indexOf(Math.max(...actionScores));
        }
        if (Math.random() < this.epsilon) {
            return Math.floor(Math.random() * this.actions.length);
        }
        const actionScores = this.qTable[state] || new Array(this.actions.length).fill(0);
        return actionScores.indexOf(Math.max(...actionScores));
    }

    // === FIXED INJECT FUNCTION - ENGLISH ONLY ===
    injectDominantUiTransformation(actionIdx) {
        const actionName = this.actions[actionIdx];
        console.log(`%c[Performance-Max-ACTUATOR MAX] Injecting Matrix Action: ${actionName}`, "color: #ccff00; font-weight: bold;");

        const headlineNode = document.querySelector('h1');

        if (headlineNode) {
            switch (actionName) {
                case 'VARIANT_PROMO_AGGRESSIVE':
                    headlineNode.innerHTML = `8000Kicks — <span style="color:#ff3366; font-weight:900;">35% OFF LIMITED TIME</span> Waterproof Hemp Shoes!`;
                    break;
                case 'VARIANT_URGENCY_SCARCITY':
                    headlineNode.innerHTML = `⚡ LAST CHANCE: Only <span style="color: #ffbd03; font-weight: 900;">12 PAIRS LEFT</span> in Stock!`;
                    break;
                case 'VARIANT_HYPER_SOCIAL_PROOF':
                    headlineNode.innerHTML = `⭐ 4,921 REAL USERS Verified: The Best Waterproof Hemp Shoes 2026!`;
                    break;
                case 'VARIANT_DYNAMIC_OFFER':
                    headlineNode.innerHTML = `🚀 SPECIAL OFFER: Get $80 Voucher when purchasing within 15 minutes!`;
                    break;
                case 'VARIANT_SEO_AEO_PUSH':
                    headlineNode.innerHTML = `🌟 #1 Waterproof Hemp Shoes 2026 — Trusted by 4,921 Real Users!`;
                    break;
                case 'VARIANT_TRUST_MAX':
                    headlineNode.innerHTML = `✅ 100% AUTHENTIC | 2-Year Warranty | Free Returns within 30 Days`;
                    break;
            }
        }
    }

    igniteEngine() {
        window.addEventListener('load', () => {
            const optimalActionTarget = this.stochasticActionSelection(this.currentState);
            this.injectDominantUiTransformation(optimalActionTarget);
        });
    }
}

if (typeof window !== 'undefined') {
    window.addEventListener('load', () => {
        if (!window.PerformanceMaxBrain) {
            window.PerformanceMaxBrain = new UltimatePerformanceMaxAgent();
            console.log('%c[Performance-Max.js v4.0-ULTIMA-MAX] Initialized with ENGLISH ONLY content', 'color: #00ff66; font-weight: bold;');
        }
    });
}