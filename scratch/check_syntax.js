const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('c:/Users/EARTH/OneDrive/Desktop/Antigravity 2026/Astro AI app/index.html', 'utf8');

// Extract all <script> contents from index.html
const scriptRegex = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;
let match;
let count = 0;
let errors = 0;

while ((match = scriptRegex.exec(html)) !== null) {
  count++;
  const code = match[1];
  if (!code.trim()) continue;
  try {
    new vm.Script(code);
    console.log(`Script block #${count}: OK`);
  } catch (err) {
    errors++;
    console.error(`Script block #${count} SYNTAX ERROR:`, err.message);
    const lines = code.split('\n');
    // find error line if possible
    console.error(`Line snippet:`, err.stack.split('\n')[0]);
  }
}

if (errors === 0) {
  console.log("All script blocks have valid JS syntax!");
} else {
  console.log(`Found ${errors} syntax errors!`);
}
