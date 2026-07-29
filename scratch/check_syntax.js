const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

// Extract all <script> contents and validate syntax
const scriptRegex = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;
let match;
let scriptIndex = 0;
let errors = 0;

while ((match = scriptRegex.exec(html)) !== null) {
  const scriptContent = match[1];
  // Skip external scripts with src
  if (!scriptContent.trim()) continue;
  
  scriptIndex++;
  try {
    new Function(scriptContent);
    console.log(`Script ${scriptIndex}: OK`);
  } catch (err) {
    console.error(`Script ${scriptIndex} Syntax Error:`, err.message);
    errors++;
  }
}

if (errors === 0) {
  console.log("All inline scripts compiled successfully with 0 syntax errors!");
} else {
  console.error(`Found ${errors} script syntax error(s).`);
  process.exit(1);
}
