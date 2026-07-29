const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

console.log("=== TESTING GOAL PREDICTION GENERATION FOR PRATEEK VS SONAM ===");

// Check if static text still exists or if dynamic generator replaced it
if (html.includes("Your 10th house lord and its position in the chart indicate the nature of your career path")) {
  console.log("CRITICAL ERROR: Static text still found in index.html!");
} else {
  console.log("SUCCESS: Static text block completely eliminated from index.html!");
}

if (html.includes("generateDynamicGoalPrediction")) {
  console.log("SUCCESS: generateDynamicGoalPrediction function is present and integrated into generateChart!");
} else {
  console.log("ERROR: generateDynamicGoalPrediction not found!");
}
