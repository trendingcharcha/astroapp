const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

console.log("=== CHECKING ALL RENDER FUNCTIONS IN INDEX.HTML ===");

const renderFuncs = html.match(/function\s+(render[a-zA-Z0-9_]+|generate[a-zA-Z0-9_]+)\s*\(/g);
console.log("Found render/generate functions:", renderFuncs);

// Search for any remaining hardcoded strings in render functions
const staticHighlights = [];
const lines = html.split('\n');
lines.forEach((line, idx) => {
  if (line.includes('Phase 1:') || line.includes('65%') || line.includes('Raj Yoga Active') || line.includes('Intellectual & Sharp') || line.includes('Wear Pearl')) {
    staticHighlights.push(`Line ${idx+1}: ${line.trim()}`);
  }
});

console.log("\nHardcoded strings found on lines:");
staticHighlights.forEach(l => console.log(l));
