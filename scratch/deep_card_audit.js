const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

console.log("=== COMPREHENSIVE CARD-BY-CARD AUDIT OF ASTRO AI APP ===\n");

// 1. Find all card containers in HTML
const cardRegex = /<div\b[^>]*class="[^"]*card[^"]*"[^>]*>([\s\S]*?)<\/div>/gi;
const cardIds = [];
const elementIdRegex = /id="([^"]+)"/g;

let match;
const idsFound = new Set();
while ((match = elementIdRegex.exec(html)) !== null) {
  idsFound.add(match[1]);
}

console.log(`Total unique element IDs in index.html: ${idsFound.size}`);

// Verify key data injection targets across all 6 tabs
const tabAudit = {
  "HOME TAB": [
    'user-header-name', 'user-streak-count', 'user-xp-count',
    'q-vedic-text', 'q-lalkitab-text', 'q-vastu-text', 'q-practical-text',
    'journey-day-navigator', 'roadmap-tasks-container', 'panchang-card', 'horoscope-card'
  ],
  "KUNDLI TAB": [
    'result-name', 'result-subtitle', 'k-lagna-name', 'k-lagna-lord', 'k-lagna-nakshatra',
    'placements-tbody', 'k-moon-nakshatra', 'k-current-dasha', 'k-dosha-list',
    'k-houses-list', 'k-strength-list', 'k-prediction-en'
  ],
  "LAL KITAB TAB": [
    'lalkitab-chart-canvas', 'lk-mangal-details', 'lk-budh-details', 'lk-teva-details', 'lk-remedies-details'
  ],
  "MATCHING TAB": [
    'm-p1-name', 'm-p2-name', 'matching-couple-title', 'matching-gun-score',
    'matching-rashi-score', 'matching-biz-score', 'matching-marriage-score', 'matching-verdict'
  ],
  "VASTU TAB": [
    'vastu-lagna-name', 'vastu-element-name', 'vastu-power-dir',
    'v-house-text', 'v-business-text', 'v-sleep-text', 'v-food-text'
  ],
  "COACH TAB": [
    'c-name', 'c-goal', 'c-profession', 'c-custom-issue',
    'coach-result-title', 'coach-astrological-prediction',
    'vedic-tasks-list', 'lalkitab-tasks-list', 'vastu-tasks-list', 'practical-tasks-list'
  ]
};

let allTargetsExist = true;
for (const [tabName, targetIds] of Object.entries(tabAudit)) {
  console.log(`\n--- ${tabName} ---`);
  targetIds.forEach(id => {
    const exists = idsFound.has(id);
    console.log(`  [${exists ? 'EXISTS' : 'MISSING'}] ID: ${id}`);
    if (!exists) allTargetsExist = false;
  });
}

console.log(`\nAll critical UI card element IDs present: ${allTargetsExist ? 'YES' : 'NO'}`);
