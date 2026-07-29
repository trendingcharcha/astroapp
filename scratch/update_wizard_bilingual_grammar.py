with open('index.html', 'rb') as f:
    content = f.read().decode('utf-8')

old_js_engine_start = "// ═══════════════════════════════════════════════════════════════\n// LIVE AI TASK ADAPTER WIZARD ENGINE (4-STEP INTERACTIVE FLOW)\n// ═══════════════════════════════════════════════════════════════"
old_js_engine_end = "showToast(currentAppLang === 'hi' ? 'कार्य विकल्प संपन्न! +20 XP प्रदान किया गया।' : `Alternative ${taskType.toUpperCase()} task completed! +20 XP awarded.`);\n}"

new_bilingual_wizard_engine = '''// ═══════════════════════════════════════════════════════════════
// LIVE AI KARMA ASSISTANT WIZARD ENGINE (BILINGUAL & GRAMMAR FIXED)
// ═══════════════════════════════════════════════════════════════
let wizardState = {
  q1_issue: '',
  q2_selected_tasks: [],
  q3_location: '',
  generatedAlternatives: {}
};

function openLiveChatModal() {
  const modal = document.getElementById('livechat-modal');
  if (!modal) return;
  modal.style.display = 'flex';
  
  // Reset wizard state and start Q1 flow
  wizardState = { q1_issue: '', q2_selected_tasks: [], q3_location: '', generatedAlternatives: {} };
  const msgContainer = document.getElementById('livechat-messages');
  if (msgContainer) {
    msgContainer.innerHTML = '';
    startWizardStep1();
  }
}

function closeLiveChatModal() {
  const modal = document.getElementById('livechat-modal');
  if (modal) modal.style.display = 'none';
}

function appendChatMessage(sender, htmlContent) {
  const msgContainer = document.getElementById('livechat-messages');
  if (!msgContainer) return;

  const msgDiv = document.createElement('div');
  msgDiv.style.maxWidth = '92%';
  msgDiv.style.padding = '10px 14px';
  msgDiv.style.borderRadius = '12px';
  msgDiv.style.fontSize = '0.82rem';
  msgDiv.style.lineHeight = '1.5';

  if (sender === 'user') {
    msgDiv.style.alignSelf = 'flex-end';
    msgDiv.style.background = 'linear-gradient(135deg, #6c5ce7, #8e44ad)';
    msgDiv.style.color = '#fff';
    msgDiv.style.borderBottomRightRadius = '2px';
    msgDiv.style.textAlign = 'left';
  } else {
    msgDiv.style.alignSelf = 'flex-start';
    msgDiv.style.background = 'rgba(255, 255, 255, 0.08)';
    msgDiv.style.color = '#e2e8f0';
    msgDiv.style.border = '1px solid rgba(142, 111, 214, 0.3)';
    msgDiv.style.borderBottomLeftRadius = '2px';
    msgDiv.style.textAlign = 'left';
  }

  msgDiv.innerHTML = htmlContent;
  msgContainer.appendChild(msgDiv);
  msgContainer.scrollTop = msgContainer.scrollHeight;
}

function startWizardStep1() {
  const userName = localStorage.getItem('user_name') || 'Seeker';
  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';

  const greeting = lang === 'hi'
    ? `नमस्ते <strong>${userName}</strong>! आज आपके उपायों में मैं कैसे सहायता कर सकता हूँ?<br><br><strong>Q1: आज आपका कार्य पूरा न होने का क्या कारण है?</strong><br><span style="font-size: 0.75rem; color: var(--gold);">(नीचे से 1 विकल्प चुनें)</span>`
    : `Namaste <strong>${userName}</strong>! How can I assist your remedies today?<br><br><strong>Q1: What is the issue preventing you from completing your task today?</strong><br><span style="font-size: 0.75rem; color: var(--gold);">(Select 1 option below)</span>`;

  const btn1 = lang === 'hi' ? "1️⃣ मैंने आज का विशेष कार्य छोड़ दिया" : "1️⃣ I skipped today's selective task";
  const btn2 = lang === 'hi' ? "2️⃣ मैं आज विशेष कार्य करने में असमर्थ हूँ" : "2️⃣ I am unable to perform the selective task today";
  const btn3 = lang === 'hi' ? "3️⃣ मैं जल्दी में था/थी और सुबह का कार्य भूल गया/गई" : "3️⃣ I was in a hurry and forgot my morning tasks";
  const btn4 = lang === 'hi' ? "4️⃣ मेरे पास आवश्यक सामग्री उपलब्ध नहीं है" : "4️⃣ I do not have the required task items";

  const q1HTML = `${greeting}
  <div style="margin-top: 10px; display: flex; flex-direction: column; gap: 8px; align-items: flex-start; text-align: left;">
    <button onclick="handleWizardQ1(this, '${btn1.replace(/'/g, "\\'")}')" class="btn btn-outline" style="text-align: left !important; justify-content: flex-start !important; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff; width: 100%; display: flex; align-items: center;">${btn1}</button>
    <button onclick="handleWizardQ1(this, '${btn2.replace(/'/g, "\\'")}')" class="btn btn-outline" style="text-align: left !important; justify-content: flex-start !important; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff; width: 100%; display: flex; align-items: center;">${btn2}</button>
    <button onclick="handleWizardQ1(this, '${btn3.replace(/'/g, "\\'")}')" class="btn btn-outline" style="text-align: left !important; justify-content: flex-start !important; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff; width: 100%; display: flex; align-items: center;">${btn3}</button>
    <button onclick="handleWizardQ1(this, '${btn4.replace(/'/g, "\\'")}')" class="btn btn-outline" style="text-align: left !important; justify-content: flex-start !important; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff; width: 100%; display: flex; align-items: center;">${btn4}</button>
  </div>`;
  
  appendChatMessage('assistant', q1HTML);
}

function handleWizardQ1(btn, issueText) {
  wizardState.q1_issue = issueText;
  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';
  appendChatMessage('user', lang === 'hi' ? `चयनित कारण: "${issueText}"` : `Issue Selected: "${issueText}"`);
  
  setTimeout(() => {
    startWizardStep2();
  }, 300);
}

function startWizardStep2() {
  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';
  const taskVedic = localStorage.getItem('today_quest_vedic_text') || (lang === 'hi' ? 'वैदिक मंत्र जाप' : 'Vedic Mantra Chanting');
  const taskLal = localStorage.getItem('today_quest_lalkitab_text') || (lang === 'hi' ? 'लाल किताब उपाय' : 'Lal Kitab Remedial Action');
  const taskVastu = localStorage.getItem('today_quest_vastu_text') || (lang === 'hi' ? 'वास्तु दिशा संरेखन' : 'Vastu Alignment Step');
  const taskPrac = localStorage.getItem('today_quest_practical_text') || (lang === 'hi' ? 'व्यावहारिक लक्ष्य कार्य' : 'Practical Goal Focus');

  const title = lang === 'hi'
    ? `<strong>Q2: आज जिन कार्यों के लिए आपको विकल्प चाहिए, उन्हें चुनें:</strong><br><span style="font-size: 0.75rem; color: var(--gold);">(अधिकतम 3 कार्य तक चुनें)</span>`
    : `<strong>Q2: Select the task(s) you need an alternative for today:</strong><br><span style="font-size: 0.75rem; color: var(--gold);">(Check up to MAX 3 tasks)</span>`;

  const btnText = lang === 'hi' ? "Q3 पर जाएँ (स्थान चुनें) →" : "CONTINUE TO Q3 (LOCATION) →";

  const q2HTML = `${title}
  
  <div style="margin-top: 10px; display: flex; flex-direction: column; gap: 8px; background: rgba(255,255,255,0.03); padding: 10px; border-radius: 8px; border: 1px solid rgba(142,111,214,0.3); text-align: left;">
    <label style="display: flex; align-items: flex-start; gap: 8px; cursor: pointer; font-size: 0.8rem; text-align: left;">
      <input type="checkbox" class="q2-task-cb" value="vedic" onchange="limitQ2Selections(this)" style="width: 18px; height: 18px; margin-top: 2px;">
      <span><strong>${lang === 'hi' ? 'वैदिक कार्य' : 'Vedic Task'}:</strong> ${taskVedic}</span>
    </label>
    <label style="display: flex; align-items: flex-start; gap: 8px; cursor: pointer; font-size: 0.8rem; text-align: left;">
      <input type="checkbox" class="q2-task-cb" value="lalkitab" onchange="limitQ2Selections(this)" style="width: 18px; height: 18px; margin-top: 2px;">
      <span><strong>${lang === 'hi' ? 'लाल किताब कार्य' : 'Lal Kitab Task'}:</strong> ${taskLal}</span>
    </label>
    <label style="display: flex; align-items: flex-start; gap: 8px; cursor: pointer; font-size: 0.8rem; text-align: left;">
      <input type="checkbox" class="q2-task-cb" value="vastu" onchange="limitQ2Selections(this)" style="width: 18px; height: 18px; margin-top: 2px;">
      <span><strong>${lang === 'hi' ? 'वास्तु कार्य' : 'Vastu Task'}:</strong> ${taskVastu}</span>
    </label>
    <label style="display: flex; align-items: flex-start; gap: 8px; cursor: pointer; font-size: 0.8rem; text-align: left;">
      <input type="checkbox" class="q2-task-cb" value="practical" onchange="limitQ2Selections(this)" style="width: 18px; height: 18px; margin-top: 2px;">
      <span><strong>${lang === 'hi' ? 'व्यावहारिक कार्य' : 'Practical Task'}:</strong> ${taskPrac}</span>
    </label>
  </div>
  
  <button onclick="submitWizardQ2()" class="btn" style="margin-top: 10px; padding: 8px 14px; font-size: 0.8rem; background: linear-gradient(135deg, var(--gold), #d4af37); color: #0C0922; font-weight: bold; width: 100%;">
    ${btnText}
  </button>`;

  appendChatMessage('assistant', q2HTML);
}

function limitQ2Selections(cb) {
  const checked = document.querySelectorAll('.q2-task-cb:checked');
  if (checked.length > 3) {
    cb.checked = false;
    showToast(currentAppLang === 'hi' ? 'आप अधिकतम 3 कार्य ही चुन सकते हैं!' : 'You can select a maximum of 3 tasks!');
  }
}

function submitWizardQ2() {
  const checkedEls = document.querySelectorAll('.q2-task-cb:checked');
  if (checkedEls.length === 0) {
    showToast(currentAppLang === 'hi' ? 'कृपया कम से कम 1 कार्य चुनें!' : 'Please select at least 1 task to continue!');
    return;
  }

  wizardState.q2_selected_tasks = Array.from(checkedEls).map(el => el.value);
  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';
  appendChatMessage('user', lang === 'hi' ? `विकल्प के लिए ${wizardState.q2_selected_tasks.length} कार्य चुने गए।` : `Selected ${wizardState.q2_selected_tasks.length} task(s) for alternative solution.`);

  setTimeout(() => {
    startWizardStep3();
  }, 300);
}

function startWizardStep3() {
  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';

  const title = lang === 'hi'
    ? `<strong>Q3: अभी आप कहाँ स्थित हैं?</strong><br><span style="font-size: 0.75rem; color: var(--gold);">(नीचे से 1 स्थान चुनें)</span>`
    : `<strong>Q3: Where are you located right now?</strong><br><span style="font-size: 0.75rem; color: var(--gold);">(Select 1 location below)</span>`;

  const btn1 = lang === 'hi' ? "🏠 घर पर" : "🏠 Home";
  const btn2 = lang === 'hi' ? "🏢 कार्यालय / कार्यस्थल पर" : "🏢 Office / Workplace";
  const btn3 = lang === 'hi' ? "🚗 बाहर बाजार में / यात्रा में" : "🚗 Outside in Market / Traveling";

  const q3HTML = `${title}
  
  <div style="margin-top: 10px; display: flex; flex-direction: column; gap: 8px; align-items: flex-start; text-align: left;">
    <button onclick="handleWizardQ3(this, '${btn1}')" class="btn btn-outline" style="text-align: left !important; justify-content: flex-start !important; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff; width: 100%; display: flex; align-items: center;">${btn1}</button>
    <button onclick="handleWizardQ3(this, '${btn2}')" class="btn btn-outline" style="text-align: left !important; justify-content: flex-start !important; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff; width: 100%; display: flex; align-items: center;">${btn2}</button>
    <button onclick="handleWizardQ3(this, '${btn3}')" class="btn btn-outline" style="text-align: left !important; justify-content: flex-start !important; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff; width: 100%; display: flex; align-items: center;">${btn3}</button>
  </div>`;

  appendChatMessage('assistant', q3HTML);
}

function handleWizardQ3(btn, locationText) {
  wizardState.q3_location = locationText;
  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';
  appendChatMessage('user', lang === 'hi' ? `स्थान: "${locationText}"` : `Location: "${locationText}"`);

  setTimeout(() => {
    generateStep4AlternativeSolutions();
  }, 400);
}

function generateStep4AlternativeSolutions() {
  const issue = wizardState.q1_issue;
  const tasks = wizardState.q2_selected_tasks;
  const location = wizardState.q3_location;
  const goal = (localStorage.getItem('user_goal') || 'job').toUpperCase();
  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';

  const heading = lang === 'hi'
    ? `<strong>आज के लिए सात्विक वैकल्पिक उपाय:</strong><br><span style="font-size: 0.75rem; color: var(--gold);">${location} स्थिति के अनुसार मूल्यांकित</span><br><br>`
    : `<strong>Dynamic Sattvic Alternatives for Today:</strong><br><span style="font-size: 0.75rem; color: var(--gold);">Evaluated for ${location}</span><br><br>`;

  let solutionsHTML = heading;

  tasks.forEach(taskType => {
    let altText = '';
    const isOffice = location.includes('Office') || location.includes('कार्यालय');
    const isOutside = location.includes('Outside') || location.includes('Traveling') || location.includes('बाहर') || location.includes('यात्रा');

    if (isOffice) {
      if (taskType === 'vedic') altText = lang === 'hi' ? "डेस्क जाप: अपनी डेस्क पर पूर्व दिशा की ओर मुख करके 11 बार 'ॐ नमः शिवाय' का मानसिक जाप करें" : "Desk Chant: Mentally repeat 'Om Namah Shivaya' 11x facing East at your desk";
      else if (taskType === 'lalkitab') altText = lang === 'hi' ? "कार्यस्थल सात्विकता: अपनी डेस्क पर पीने के पानी का 1 स्वच्छ गिलास रखें और 1 घूंट सहकर्मी को दें" : "Workplace Sattva: Keep 1 clean glass of drinking water on your desk and offer 1 sip to a colleague";
      else if (taskType === 'vastu') altText = lang === 'hi' ? "डेस्क वास्तु: कार्य करते समय अपने लैपटॉप/स्क्रीन को उत्तर या पूर्व दिशा की ओर रखें" : "Desk Vastu: Adjust laptop/screen to face North or East while executing work tasks";
      else altText = lang === 'hi' ? "कार्यालय कार्य: अपना अगला कार्य शुरू करने से पहले 3 बार गहरी सचेत सांसें लें" : "Office Action: Take 3 deep conscious breaths before starting your next executive task";
    } else if (isOutside) {
      if (taskType === 'vedic') altText = lang === 'hi' ? "यात्रा मंत्र: चलते या यात्रा करते समय अपने स्वामी ग्रह मंत्र का 7 बार मानसिक जाप करें" : "Travel Mantra: Silently recite your ruling planet mantra 7 times while walking/moving";
      else if (taskType === 'lalkitab') altText = lang === 'hi' ? "सार्वजनिक कर्म: बाहर रहते हुए किसी जरूरतमंद व्यक्ति या पक्षी को पानी या भोजन अर्पण करें" : "Public Karma: Offer 1 coin or food to a needy person or street bird while outside";
      else if (taskType === 'vastu') altText = lang === 'hi' ? "यात्रा दिशा: 10 सेकंड के लिए पूर्व दिशा की ओर मुख करके रुकें और अपने लक्ष्य में सफलता की कल्पना करें" : "Travel Direction: Pause facing East for 10 seconds and visualize success in your goal";
      else altText = lang === 'hi' ? "मोबाइल नोट: अपने स्मार्टफोन नोटपैड में अपने लक्ष्य के लिए 1 कार्य कदम लिखें" : "Mobile Note: Write 1 action step for your goal in your smartphone notepad";
    } else { // Home
      if (taskType === 'vedic') altText = lang === 'hi' ? "गृह सात्विकता: एक दीपक या अगरबत्ती जलाएं और 1 मिनट के लिए शांत मन से ईश्वर का स्मरण करें" : "Home Sattva: Light a lamp or incense stick and offer silent gratitude for 1 minute";
      else if (taskType === 'lalkitab') altText = lang === 'hi' ? "गृह उपाय: पौधे की हरी पत्ती को स्पर्श करें और 1 गिलास स्वच्छ जल का सेवन करें" : "Home Remedy: Touch a green leaf of an indoor plant and drink 1 glass of water";
      else if (taskType === 'vastu') altText = lang === 'hi' ? "गृह संरेखन: 2 मिनट के लिए उत्तर-पूर्व (ईशान) कोण में शांत मन से बैठें" : "Home Alignment: Sit in North-East corner for 2 minutes with calm mind";
      else altText = lang === 'hi' ? "गृह कार्य: अपनी 90-दिवसीय कर्म परिवर्तन योजना की समीक्षा के लिए 5 मिनट दें" : "Home Action: Spend 5 minutes reviewing your 90-day karmic transformation plan";
    }

    wizardState.generatedAlternatives[taskType] = altText;

    const btnLabel = lang === 'hi' ? "✓ विकल्प पूर्ण करें व +20 XP प्राप्त करें" : "✓ MARK ALTERNATIVE AS DONE & CLAIM +20 XP";

    solutionsHTML += `<div style="margin-bottom: 12px; background: rgba(232, 200, 121, 0.08); border: 1px dashed var(--gold); border-radius: 8px; padding: 10px; text-align: left;">
      <p style="margin: 0 0 4px 0; font-size: 0.75rem; color: var(--gold); font-weight: bold;">${lang === 'hi' ? 'प्रस्तावित सात्विक विकल्प' : 'PROPOSED ALTERNATIVE'} (${taskType.toUpperCase()}):</p>
      <p style="margin: 0 0 8px 0; font-size: 0.8rem; color: #fff;">"${altText}"</p>
      <button onclick="acceptWizardAlternative(this, '${taskType}')" class="btn" style="width: 100%; padding: 6px 12px; font-size: 0.78rem; background: linear-gradient(135deg, var(--gold), #d4af37); color: #0C0922; font-weight: bold; justify-content: center !important;">
        ${btnLabel}
      </button>
    </div>`;
  });

  const footerNote = lang === 'hi'
    ? "नोट: विकल्प जमा करने से केवल आज का कार्य अपडेट होता है। कल से, मुख्य स्वचालित प्रणाली सामान्य रूप से कार्य करेगी।"
    : "Note: Submitting alternative as done updates TODAY'S task only. Tomorrow, the core automated dynamic engine resumes normally.";

  solutionsHTML += `<p style="font-size: 0.72rem; color: var(--text-muted); font-style: italic; margin-top: 6px; text-align: left;">${footerNote}</p>`;

  appendChatMessage('assistant', solutionsHTML);
}

function acceptWizardAlternative(btnBtn, taskType) {
  const altText = wizardState.generatedAlternatives[taskType];
  if (!altText) return;

  const todayStr = getFormattedDate();
  localStorage.setItem(`today_quest_${taskType}_done`, 'true');
  localStorage.setItem(`today_quest_${taskType}_text`, altText);

  const textEl = document.getElementById(`q-${taskType}-text`);
  if (textEl) textEl.innerText = altText;

  const checkEl = document.getElementById(`q-${taskType}-check`);
  if (checkEl) checkEl.checked = true;

  gainXP(20);

  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';

  if (btnBtn) {
    btnBtn.disabled = true;
    btnBtn.style.background = 'linear-gradient(135deg, #2ecc71, #27ae60)';
    btnBtn.style.color = '#fff';
    btnBtn.innerText = lang === 'hi' ? '✓ विकल्प संपन्न! +20 XP प्राप्त हुआ' : '✓ ALTERNATIVE COMPLETED & +20 XP CLAIMED!';
  }

  showToast(lang === 'hi' ? 'कार्य विकल्प संपन्न! +20 XP प्रदान किया गया।' : `Alternative ${taskType.toUpperCase()} task completed! +20 XP awarded.`);
}'''

if old_js_engine_start in content and old_js_engine_end in content:
    start_pos = content.find(old_js_engine_start)
    end_pos = content.find(old_js_engine_end) + len(old_js_engine_end)
    content = content[:start_pos] + new_bilingual_wizard_engine + content[end_pos:]
    print("SUCCESS: Updated Wizard JS Engine with Bilingual EN/HI Support, Flawless Grammar, and Strict Left Alignment")
else:
    print("WARNING: Could not locate exact JS boundaries")

with open('index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print("File written.")
