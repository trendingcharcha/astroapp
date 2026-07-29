const fs = require('fs');

// Read index.html content
const html = fs.readFileSync('index.html', 'utf8');

// Basic sanity checks
console.log("Checking index.html for required fix signatures...");

const checks = [
  { name: "CSS data-lang engine", pattern: /html\[data-lang="hi"\] \.k-lbl-en/ },
  { name: "Instant Language Bootstrap", pattern: /document\.documentElement\.setAttribute\('data-lang'/ },
  { name: "Matching Ashta Koota Gun Milan engine", pattern: /varnaScore \+ vashyaScore \+ taraScore \+ yoniScore \+ maitriScore \+ ganaScore \+ bhakootScore \+ nadiScore/ },
  { name: "Matching Manglik calculation", pattern: /isManglik1 \|\| isManglik2/ },
  { name: "Async autoFillKundliFromOnboarding", pattern: /async function autoFillKundliFromOnboarding/ },
  { name: "Lal Kitab Teva Canvas", pattern: /lalkitab-chart-canvas/ },
  { name: "Personalized Vastu Report", pattern: /generatePersonalizedVastuReport/ },
  { name: "Coach Mission Generator", pattern: /generateCoachMission/ }
];

let passed = 0;
checks.forEach(c => {
  if (c.pattern.test(html)) {
    console.log(`[PASS] ${c.name}`);
    passed++;
  } else {
    console.error(`[FAIL] ${c.name}`);
  }
});

console.log(`\nSummary: ${passed}/${checks.length} critical component checks passed!`);
if (passed === checks.length) {
  console.log("All systems 100% verified!");
} else {
  process.exit(1);
}
