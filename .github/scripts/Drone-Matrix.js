/**
 * Drone-Matrix.js
 * EATHESEN V3000-Ω SOTA | Drone UX & Signal Harvesting Module + English Lock
 */

class DroneMatrix {
    constructor() {
        this.signature = "V3000-Ω-DRONE-MATRIX";
        console.log(`%c[DRONE-MATRIX] Activated - Signal Harvesting Started`, "color: #00e5ff; font-weight: bold;");
    }

    harvestSignals() {
        const signals = {
            scrollDepth: Math.round((window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100),
            timeOnPage: Math.floor(performance.now() / 1000),
            droneFocus: document.querySelectorAll('img[alt*="drone"]').length > 0
        };
        console.log(`%c[DRONE-MATRIX] Signals:`, "color: #00e5ff", signals);
        return signals;
    }

    enhanceDroneVisuals() {
        document.querySelectorAll('img[alt*="drone"]').forEach(img => {
            img.style.transition = 'all 0.4s';
            img.style.boxShadow = '0 0 20px #00e5ff';
        });
    }

    start() {
        this.harvestSignals();
        this.enhanceDroneVisuals();
        setInterval(() => this.harvestSignals(), 7000);
    }
}

if (typeof window !== 'undefined') {
    window.addEventListener('load', () => new DroneMatrix().start());
}