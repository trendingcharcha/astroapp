const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

console.log("=== COMPREHENSIVE AUDIT FOR REMAINING STATIC TEXT OR CARDS ===");

// 1. Kundli 12 House Interpretations
console.log("\n[1] Kundli 12 House Interpretations Audit:");
if (html.includes("houseSignifications")) {
  console.log("Found houseSignifications in Kundli tab.");
}

// Check where 12 House readings are rendered in Kundli tab
const houseInterpretationsMatch = html.match(/houseInterpretations\s*=\s*\[([\s\S]*?)\];/);
if (houseInterpretationsMatch) {
  console.log("FOUND houseInterpretations array! Checking if static...");
} else {
  console.log("No static houseInterpretations array found.");
}

// 2. Lal Kitab Remedies & Teva text
console.log("\n[2] Lal Kitab Remedies & Teva Audit:");
if (html.includes("generateLalKitabReport")) {
  console.log("Found generateLalKitabReport.");
}

// 3. Vastu Directives
console.log("\n[3] Vastu Directives Audit:");
if (html.includes("generatePersonalizedVastuReport")) {
  console.log("Found generatePersonalizedVastuReport.");
}

// 4. Coach Mission Predictions
console.log("\n[4] Coach Mission Predictions Audit:");
if (html.includes("generateCoachMission")) {
  console.log("Found generateCoachMission.");
}

// Search for any remaining static text objects in JS
const staticObjects = [];
const matches = html.matchAll(/(const|let|var)\s+([a-zA-Z0-9_]+)\s*=\s*\{[\s\S]*?en:\s*["'][^"']{50,}["']/g);
for (const m of matches) {
  staticObjects.push(m[2]);
}
console.log("\nStatic text objects with long 'en' strings found in JS:", staticObjects);
