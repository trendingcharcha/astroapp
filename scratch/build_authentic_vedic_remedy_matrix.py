with open('index.html', 'rb') as f:
    content = f.read().decode('utf-8')

# Replace generateStep4AlternativeSolutions with authentic Vedic planetary substitution matrix
old_step4_fn = '''function generateStep4AlternativeSolutions() {
  const issue = wizardState.q1_issue;
  const taskIndices = wizardState.q2_selected_tasks;
  const location = wizardState.q3_location;
  const goal = (localStorage.getItem('user_goal') || 'job').toUpperCase();
  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';

  const heading = lang === 'hi'
    ? `<strong>आज के लिए सात्विक वैकल्पिक उपाय:</strong><br><span style="font-size: 0.75rem; color: var(--gold);">${location} स्थिति के अनुसार मूल्यांकित</span><br><br>`
    : `<strong>Dynamic Sattvic Alternatives for Today:</strong><br><span style="font-size: 0.75rem; color: var(--gold);">Evaluated for ${location}</span><br><br>`;

  let solutionsHTML = heading;
  const liveTasks = getLiveDashboardDoableTasks();

  taskIndices.forEach(taskIdx => {
    const taskObj = liveTasks.find(t => String(t.index) === String(taskIdx)) || { title: 'Task', text: 'Daily Remedy' };
    let altText = '';
    const isOffice = location.includes('Office') || location.includes('कार्यालय');
    const isOutside = location.includes('Outside') || location.includes('Traveling') || location.includes('बाहर') || location.includes('यात्रा');

    if (isOffice) {
      altText = lang === 'hi'
        ? `डेस्क कार्य: अपनी कार्यस्थल डेस्क पर पूर्व की ओर मुख करके 3 बार सचेत सांसें लें और '${taskObj.title}' के लिए मानसिक प्रार्थना करें`
        : `Desk Action for ${taskObj.title}: Sit upright at your desk facing East, take 3 conscious breaths and repeat short mental prayer`;
    } else if (isOutside) {
      altText = lang === 'hi'
        ? `यात्रा कार्य: यात्रा के दौरान '${taskObj.title}' के लिए स्वामी ग्रह मंत्र का 7 बार मानसिक स्मरण करें`
        : `Travel Action for ${taskObj.title}: Silently repeat ruling planet mantra 7 times while walking or traveling`;
    } else {
      altText = lang === 'hi'
        ? `गृह सात्विक कार्य: घर पर उत्तर-पूर्व दिशा में 2 मिनट बैठें और '${taskObj.title}' संकल्प दोहराएं`
        : `Home Sattva Action for ${taskObj.title}: Sit in North-East corner for 2 minutes and focus on goal success`;
    }

    wizardState.generatedAlternatives[taskIdx] = altText;
    const btnLabel = lang === 'hi' ? "✓ विकल्प पूर्ण करें व +20 XP प्राप्त करें" : "✓ MARK ALTERNATIVE AS DONE & CLAIM +20 XP";

    solutionsHTML += `<div style="margin-bottom: 12px; background: rgba(232, 200, 121, 0.08); border: 1px dashed var(--gold); border-radius: 8px; padding: 10px; text-align: left;">
      <p style="margin: 0 0 4px 0; font-size: 0.75rem; color: var(--gold); font-weight: bold;">${lang === 'hi' ? 'प्रस्तावित विकल्प' : 'PROPOSED ALTERNATIVE'} (${taskObj.title.toUpperCase()}):</p>
      <p style="margin: 0 0 8px 0; font-size: 0.8rem; color: #fff;">"${altText}"</p>
      <button onclick="acceptWizardAlternative(this, '${taskIdx}')" class="btn" style="width: 100%; padding: 6px 12px; font-size: 0.78rem; background: linear-gradient(135deg, var(--gold), #d4af37); color: #0C0922; font-weight: bold; justify-content: center !important;">
        ${btnLabel}
      </button>
    </div>`;
  });

  const footerNote = lang === 'hi'
    ? "नोट: विकल्प जमा करने से केवल आज का कार्य अपडेट होता है। कल से, मुख्य स्वचालित प्रणाली सामान्य रूप से कार्य करेगी।"
    : "Note: Submitting alternative as done updates TODAY'S task only. Tomorrow, the core automated dynamic engine resumes normally.";

  solutionsHTML += `<p style="font-size: 0.72rem; color: var(--text-muted); font-style: italic; margin-top: 6px; text-align: left;">${footerNote}</p>`;

  appendChatMessage('assistant', solutionsHTML);
}'''

new_step4_fn = '''function generateAuthenticVedicAlternative(taskTitle, taskText, location, issue) {
  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';
  const textLower = (taskTitle + " " + taskText).toLowerCase();
  const isOffice = location.includes('Office') || location.includes('कार्यालय');
  const isOutside = location.includes('Outside') || location.includes('Traveling') || location.includes('बाहर') || location.includes('यात्रा');

  // 1. MARS / TUESDAY / HANUMAN / COURAGE / DEBT REMEDIES
  if (textLower.includes('tuesday') || textLower.includes('mars') || textLower.includes('hanuman') || textLower.includes('bhaumaya') || textLower.includes('मंगल')) {
    if (isOffice) {
      return lang === 'hi'
        ? "कार्यस्थल मङ्गल ऊर्जा: अपनी डेस्क पर 11 बार 'ॐ हनुमते नमः' का मानसिक जाप करें, या ऋण बाधाओं को शांत करने के लिए किसी सहकर्मी को 1 स्वच्छ पानी का गिलास दें।"
        : "Workplace Mars Energy: Mentally chant 'Om Hanumate Namah' 11 times at your desk, or offer a glass of clean water to a colleague to dissolve debt obstacles.";
    } else if (isOutside) {
      return lang === 'hi'
        ? "यात्रा मङ्गल ऊर्जा: यात्रा के दौरान आवारा पशुओं/पक्षियों को कुछ भोजन दें, या मन में 7 बार 'ॐ हनुमते नमः' का जाप करें।"
        : "Travel Mars Energy: Offer biscuits or grain to street animals/birds while traveling, or silently repeat 'Om Hanumate Namah' 7 times.";
    } else { // Home
      return lang === 'hi'
        ? "गृह मङ्गल सात्विकता: 11 बार 'ॐ हनुमते नमः' का जाप करें, या दक्षिण दिशा की ओर मुख करके दीपक/अगरबत्ती जलाएं।"
        : "Home Mars Sattva: Recite 'Om Hanumate Namah' 11 times, or light a lamp facing South for courage and debt clearance.";
    }
  }

  // 2. VEDIC MANTRA / SHIVA / VISHNU / MERCURY REMEDIES
  if (textLower.includes('vedic') || textLower.includes('shivaya') || textLower.includes('budhaya') || textLower.includes('vishnu') || textLower.includes('मंत्र') || textLower.includes('जाप')) {
    if (isOffice) {
      return lang === 'hi'
        ? "डेस्क वैदिक जाप: अपनी डेस्क पर पूर्व की ओर मुख करके बैठें, 3 गहरी सांसें लें और मन में 11 बार 'ॐ नमः शिवाय' दोहराएं।"
        : "Desk Vedic Chant: Sit upright facing East at your desk, take 3 deep breaths, and mentally repeat 'Om Namah Shivaya' 11 times.";
    } else if (isOutside) {
      return lang === 'hi'
        ? "यात्रा मंत्र जाप: चलते या यात्रा करते समय मन ही मन 7 बार 'ॐ नमः शिवाय' का स्मरण करें।"
        : "Travel Vedic Chanting: Repeat 'Om Namah Shivaya' 7 times silently in your mind while walking or traveling.";
    } else { // Home
      return lang === 'hi'
        ? "गृह वैदिक अनुष्ठान: शांत मन से पूर्व या उत्तर की ओर मुख करके 11 बार 'ॐ नमः शिवाय' का जाप करें।"
        : "Home Vedic Ritual: Recite 'Om Namah Shivaya' 11 times with calm mind facing East or North.";
    }
  }

  // 3. LAL KITAB REMEDIES & PHYSICAL ITEMS
  if (textLower.includes('lalkitab') || textLower.includes('banyan') || textLower.includes('milk') || textLower.includes('silver') || textLower.includes('lentil') || textLower.includes('लाल किताब') || textLower.includes('उपाय')) {
    if (isOffice) {
      return lang === 'hi'
        ? "कार्यस्थल लाल किताब सात्विकता: अपनी डेस्क पर पीने के पानी का 1 स्वच्छ गिलास रखें और 3 सचेत घूंट ग्रह शांति संकल्प के साथ लें।"
        : "Workplace Lal Kitab Sattva: Keep 1 clean glass of drinking water on your desk and take 3 conscious sips dedicated to planetary peace.";
    } else if (isOutside) {
      return lang === 'hi'
        ? "सार्वजनिक कर्म: बाहर रहते हुए किसी जरूरतमंद व्यक्ति या पक्षी को पानी या भोजन अर्पण करें।"
        : "Public Lal Kitab Karma: Offer 1 coin or food item to a needy person or street bird while traveling outside.";
    } else { // Home
      return lang === 'hi'
        ? "गृह लाल किताब उपाय: घर के पौधे की हरी पत्ती को स्पर्श करें और शांत मन से 1 गिलास स्वच्छ जल ग्रहण करें।"
        : "Home Lal Kitab Remedy: Touch a green leaf of an indoor plant and consume 1 glass of fresh water with a calm mind.";
    }
  }

  // 4. VASTU & DIRECTIONAL ALIGNMENTS
  if (textLower.includes('vastu') || textLower.includes('direction') || textLower.includes('ishana') || textLower.includes('north') || textLower.includes('वास्तु') || textLower.includes('दिशा')) {
    if (isOffice) {
      return lang === 'hi'
        ? "डेस्क वास्तु संरेखन: अपनी डेस्क से 2 मिनट के लिए कागजी कचरा साफ़ करें और अपनी स्क्रीन को उत्तर या पूर्व दिशा की ओर रखें।"
        : "Desk Vastu Alignment: Clear paper clutter off your desk surface for 2 minutes and position your screen facing North or East.";
    } else if (isOutside) {
      return lang === 'hi'
        ? "यात्रा दिशा ध्यान: 10 सेकंड के लिए पूर्व की ओर मुख करके रुकें और अपने लक्ष्य में सफलता का ध्यान करें।"
        : "Travel Direction Focus: Pause facing East for 10 seconds, close your eyes, and visualize success in your goal.";
    } else { // Home
      return lang === 'hi'
        ? "गृह वास्तु संरेखन: कमरे के उत्तर-पूर्व (ईशान) कोण में 2 मिनट के लिए स्वच्छ मुद्रा में शांत बैठें।"
        : "Home Vastu Alignment: Sit quietly in the North-East corner of your room for 2 minutes with clean posture and focus.";
    }
  }

  // 5. PRACTICAL / DEBT ACTION STEPS
  if (textLower.includes('debt') || textLower.includes('action') || textLower.includes('interest') || textLower.includes('ledger') || textLower.includes('कार्य') || textLower.includes('ऋण')) {
    if (isOffice) {
      return lang === 'hi'
        ? "कार्यालय लक्ष्य कार्य: अपने स्मार्टफोन नोटपैड या वर्क प्लानर में 1 वित्तीय प्राथमिकता बिंदु लिखें।"
        : "Office Goal Action: Take 2 minutes to write 1 financial priority item in your smartphone notepad or work planner.";
    } else if (isOutside) {
      return lang === 'hi'
        ? "यात्रा लक्ष्य ध्यान: अपने फोन नोटपैड में अपने मुख्य लक्ष्य की समीक्षा करें और आज 1 कार्य कदम तय करें।"
        : "Travel Goal Focus: Review your primary monthly goal in your phone notepad and commit to 1 action step today.";
    } else { // Home
      return lang === 'hi'
        ? "गृह लक्ष्य ध्यान: अपने ऋण मुक्ति बहीखाते या मासिक बचत योजना की समीक्षा के लिए 3 मिनट दें।"
        : "Home Goal Focus: Spend 3 minutes reviewing your debt clearance ledger or monthly savings plan.";
    }
  }

  // Fallback
  return isOffice
    ? (lang === 'hi' ? "डेस्क ऊर्जा संरेखन: पूर्व की ओर मुख करके 3 बार गहरी सांसें लें और अपने लक्ष्य संकल्प का 3 बार मानसिक जाप करें।" : "Desk Energy Alignment: Take 3 deep conscious breaths facing East at your desk and repeat your goal affirmation 3 times.")
    : (lang === 'hi' ? "गृह ऊर्जा संरेखन: उत्तर-पूर्व दिशा में 2 मिनट बैठें और अपने जीवन लक्ष्य में सफलता का ध्यान करें।" : "Home Energy Alignment: Sit in a quiet room facing North-East for 2 minutes and focus on goal success.");
}

function generateStep4AlternativeSolutions() {
  const issue = wizardState.q1_issue;
  const taskIndices = wizardState.q2_selected_tasks;
  const location = wizardState.q3_location;
  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';

  const heading = lang === 'hi'
    ? `<strong>आज के लिए सात्विक ग्रह-अनुकूल वैकल्पिक उपाय:</strong><br><span style="font-size: 0.75rem; color: var(--gold);">${location} स्थिति के लिए मूल्यांकित</span><br><br>`
    : `<strong>Authentic Sattvic Planetary Alternatives for Today:</strong><br><span style="font-size: 0.75rem; color: var(--gold);">Evaluated for ${location}</span><br><br>`;

  let solutionsHTML = heading;
  const liveTasks = getLiveDashboardDoableTasks();

  taskIndices.forEach(taskIdx => {
    const taskObj = liveTasks.find(t => String(t.index) === String(taskIdx)) || { title: 'Task', text: 'Daily Remedy' };
    const altText = generateAuthenticVedicAlternative(taskObj.title, taskObj.text, location, issue);
    wizardState.generatedAlternatives[taskIdx] = altText;

    const btnLabel = lang === 'hi' ? "✓ विकल्प पूर्ण करें व +20 XP प्राप्त करें" : "✓ MARK ALTERNATIVE AS DONE & CLAIM +20 XP";

    solutionsHTML += `<div style="margin-bottom: 12px; background: rgba(232, 200, 121, 0.08); border: 1px dashed var(--gold); border-radius: 8px; padding: 10px; text-align: left;">
      <p style="margin: 0 0 4px 0; font-size: 0.75rem; color: var(--gold); font-weight: bold;">${lang === 'hi' ? 'प्रस्तावित वैदिक विकल्प' : 'PROPOSED PLANETARY ALTERNATIVE'} (${taskObj.title.toUpperCase()}):</p>
      <p style="margin: 0 0 8px 0; font-size: 0.82rem; color: #fff; line-height: 1.5;">"${altText}"</p>
      <button onclick="acceptWizardAlternative(this, '${taskIdx}')" class="btn" style="width: 100%; padding: 6px 12px; font-size: 0.78rem; background: linear-gradient(135deg, var(--gold), #d4af37); color: #0C0922; font-weight: bold; justify-content: center !important;">
        ${btnLabel}
      </button>
    </div>`;
  });

  const footerNote = lang === 'hi'
    ? "नोट: विकल्प जमा करने से केवल आज का कार्य अपडेट होता है। कल से, मुख्य स्वचालित प्रणाली सामान्य रूप से कार्य करेगी।"
    : "Note: Submitting alternative as done updates TODAY'S task only. Tomorrow, the core automated dynamic engine resumes normally.";

  solutionsHTML += `<p style="font-size: 0.72rem; color: var(--text-muted); font-style: italic; margin-top: 6px; text-align: left;">${footerNote}</p>`;

  appendChatMessage('assistant', solutionsHTML);
}'''

if old_step4_fn in content:
    content = content.replace(old_step4_fn, new_step4_fn, 1)
    print("SUCCESS: Built authentic Parashari & Lal Kitab planetary substitution matrix for Step 4")
else:
    print("WARNING: Could not find old_step4_fn")

with open('index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print("File written.")
