const fs = require('fs');
const html = fs.readFileSync('c:/Users/EARTH/OneDrive/Desktop/Antigravity 2026/Astro AI app/index.html', 'utf8');

const scriptRegex = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;
let match;
let count = 0;

while ((match = scriptRegex.exec(html)) !== null) {
  count++;
  if (count === 5) {
    const code = match[1];
    const lines = code.split('\n');
    console.log("Script block 5 total lines:", lines.length);
    // Line 4682
    for (let i = Math.max(0, 4675); i < Math.min(lines.length, 4690); i++) {
      console.log(`${i + 1}: ${lines[i]}`);
    }
  }
}
