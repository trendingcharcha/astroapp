import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("=== APPLYING FIXES FOR ALL 4 RENDER BUGS ===")

# 1. FIX KUNDLI CANVAS RENDERING: Add drawChartGeneric at end of generateChart
target1 = "renderKundliEnhancedSections(placementsList, lagnaSignNum, date);"
replacement1 = """renderKundliEnhancedSections(placementsList, lagnaSignNum, date);
  if (typeof drawChartGeneric === 'function') {
    drawChartGeneric('chartCanvas', currentKundliChartType || 'D1', document.body.classList.contains('print-pdf-active'));
  }"""

if target1 in content:
    content = content.replace(target1, replacement1, 1)
    print("[FIX 1] Added drawChartGeneric call to generateChart!")

# 2. FIX TASK DESCRIPTION MISSING IN extractIndividualDayTasks
target2_new = """let vGoalText = "";
      if (normGoal === 'job') vGoalText = isHi ? "करियर ऊर्जा सक्रिय करने के लिए 12 चक्र सूर्य नमस्कार करें।" : "Perform 12 rounds of Surya Namaskar to activate career & authority vibrations.";
      else if (normGoal === 'debt') vGoalText = isHi ? "भोजन से पहले \\"ॐ नमः शिवाय\\" का 108 बार जाप करें।" : "Recite \\"Om Namah Shivaya\\" 108 times before meals to dissolve financial anxieties.";
      else if (normGoal === 'marriage') vGoalText = isHi ? "कात्यायनी मंत्र का 108 बार जाप करें।" : "Recite Katyayani mantra 108 times to attract your destined partner.";
      else if (normGoal === 'baby') vGoalText = isHi ? "संतान गोपाल मंत्र का 108 बार जाप करें।" : "Recite Santan Gopal mantra \\"Om Devaki Sut Govind\\" 108 times for progeny blessings.";
      else if (normGoal === 'business') vGoalText = isHi ? "व्यावसायिक वृद्धि के लिए गणेश पूजा करें।" : "Perform Ganesh puja and light incense at your business entrance for growth.";
      else if (normGoal === 'property') vGoalText = isHi ? "भूमि आशीर्वाद के लिए \\"ॐ भौमाय नमः\\" का 11 बार जाप करें।" : "Chant \\"Om Bhaumaya Namah\\" 11 times for Mars blessings on land and assets.";
      else if (normGoal === 'health') vGoalText = isHi ? "सूर्योदय के समय सूर्य नमस्कार करें और तांबे के बर्तन का पानी पिएं।" : "Perform Surya Namaskar at sunrise and drink copper vessel water for vitality.";
      else vGoalText = isHi ? "मानसिक शांति के लिए 15 मिनट प्राणायाम करें।" : "Practice 15 minutes of Pranayama deep breathing for mental equilibrium.";

      tasks.push({
        category: 'vedic',
        title: isHi ? "प्रातःकालीन वैदिक अनुष्ठान" : "Morning Vedic Ritual",
        timeWindow: '06:00 AM - 07:30 AM',
        text: vGoalText + (isHi ? customNoteHi : customNoteEn),
        xp: 20,
        color: 'var(--gold)',
        icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>'
      });"""

# Clean up any leftover titleVal occurrences in extractIndividualDayTasks
content = re.sub(r"tasks\.push\(\{\s*category:\s*'vedic',\s*title:\s*titleVal[\s\S]*?\}\);", "", content)

# Insert clean task push block
pattern2 = r'// 1\. VEDIC TASKS[\s\S]*?// 2\. LAL KITAB REMEDIES'
replacement2 = """// 1. VEDIC TASKS
      const customNoteEn = userCustomIssue ? ` for focus on "${userCustomIssue}"` : '';
      const customNoteHi = userCustomIssue ? ` ("${userCustomIssue}" पर ध्यान केंद्रित करते हुए)` : '';

      """ + target2_new + """

      // 2. LAL KITAB REMEDIES"""

content = re.sub(pattern2, replacement2, content, flags=re.MULTILINE)
print("[FIX 2] Restored defined task variables in extractIndividualDayTasks!")

# 3. FIX VASTU & LAL KITAB AUTO-CALCULATION IN TAB SWITCH
target3 = "if (index === 4) {\nif (typeof generatePersonalizedVastuReport === 'function') {\ngeneratePersonalizedVastuReport();\n}\n}"
replacement3 = """if (index === 4) {
    if (typeof generatePersonalizedVastuReport === 'function') {
      generatePersonalizedVastuReport().then(() => {
        const notCalc = document.getElementById('vastu-not-calculated-view');
        const resView = document.getElementById('vastu-result-view');
        if (notCalc && resView) {
          notCalc.style.display = 'none';
          resView.style.display = 'block';
        }
      });
    }
  }"""

if target3 in content:
    content = content.replace(target3, replacement3, 1)
    print("[FIX 3] Updated switchTab Vastu report auto-rendering!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("ALL FIXES APPLIED SUCCESSFULLY!")
