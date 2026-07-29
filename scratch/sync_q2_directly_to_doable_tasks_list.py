with open('index.html', 'rb') as f:
    content = f.read().decode('utf-8')

# Replace startWizardStep2 and acceptWizardAlternative to dynamically parse #doable-tasks-list from DOM
old_wizard_q2_code = '''function getCleanShortTaskText(cat) {
  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';
  const el = document.getElementById(`q-${cat}-text`);
  if (el) {
    let txt = el.innerText || el.textContent || '';
    txt = txt.trim();
    if (txt) {
      const lines = txt.split('\\n').map(l => l.trim()).filter(l => l.length > 0);
      if (lines.length > 0) {
        let firstLine = lines[0];
        if (firstLine.length > 110) firstLine = firstLine.substring(0, 110) + '...';
        return firstLine;
      }
    }
  }
  const raw = localStorage.getItem(`today_quest_${cat}_text`) || '';
  if (raw) {
    let clean = raw.replace(/<[^>]*>?/gm, '').trim();
    const lines = clean.split('\\n').map(l => l.trim()).filter(l => l.length > 0);
    if (lines.length > 0) {
      let firstLine = lines[0];
      if (firstLine.length > 110) firstLine = firstLine.substring(0, 110) + '...';
      return firstLine;
    }
  }
  const defaultMapEn = {
    vedic: 'Vedic Ruling Planet Morning Chanting',
    lalkitab: 'Lal Kitab Daily Remedial Action',
    vastu: 'Vastu Directional Element Alignment',
    practical: 'Practical Goal Execution Step'
  };
  const defaultMapHi = {
    vedic: 'वैदिक ग्रह मंत्र जाप',
    lalkitab: 'लाल किताब दैनिक उपाय',
    vastu: 'वास्तु दिशा संरेखन',
    practical: 'व्यावहारिक लक्ष्य कार्य'
  };
  return lang === 'hi' ? defaultMapHi[cat] : defaultMapEn[cat];
}

function startWizardStep2() {
  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';
  const taskVedic = getCleanShortTaskText('vedic');
  const taskLal = getCleanShortTaskText('lalkitab');
  const taskVastu = getCleanShortTaskText('vastu');
  const taskPrac = getCleanShortTaskText('practical');

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
}'''

new_wizard_q2_code = '''function getLiveDashboardDoableTasks() {
  const container = document.getElementById('doable-tasks-list');
  const tasks = [];

  if (container) {
    const cards = container.querySelectorAll('.card, [class*="card"]');
    cards.forEach((card, idx) => {
      const titleEl = card.querySelector('h4, strong, [class*="title"]');
      const textEl = card.querySelector('p, div:nth-child(2)');

      let title = titleEl ? titleEl.innerText.trim() : `Task ${idx + 1}`;
      let text = textEl ? textEl.innerText.trim() : card.innerText.trim();

      if (text.includes(title)) {
        text = text.replace(title, '').trim();
      }
      // Remove XP badge text like "+20 XP" or "+15 XP"
      text = text.replace(/\\+\\d+\\s*XP/gi, '').trim();

      if (text.length > 85) {
        text = text.substring(0, 85) + '...';
      }

      if (title && text) {
        tasks.push({ index: idx, title: title, text: text });
      }
    });
  }

  // Fallback if container not rendered yet
  if (tasks.length === 0) {
    tasks.push({ index: 0, title: 'Morning Vedic Ritual', text: 'Chant Om Namah Shivaya 108 times before meals' });
    tasks.push({ index: 1, title: 'Lal Kitab Remedy', text: 'Offer sweet milk to a banyan tree root' });
    tasks.push({ index: 2, title: 'Personalized Direction Alignment', text: 'Face North while working or meditating' });
    tasks.push({ index: 3, title: 'Action Step', text: 'Review daily goal action items' });
  }

  return tasks;
}

function startWizardStep2() {
  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';
  const liveTasks = getLiveDashboardDoableTasks();

  const title = lang === 'hi'
    ? `<strong>Q2: आज जिन कार्यों के लिए आपको विकल्प चाहिए, उन्हें चुनें:</strong><br><span style="font-size: 0.75rem; color: var(--gold);">(अधिकतम 3 कार्य तक चुनें)</span>`
    : `<strong>Q2: Select the task(s) you need an alternative for today:</strong><br><span style="font-size: 0.75rem; color: var(--gold);">(Check up to MAX 3 tasks)</span>`;

  const btnText = lang === 'hi' ? "Q3 पर जाएँ (स्थान चुनें) →" : "CONTINUE TO Q3 (LOCATION) →";

  let tasksChecklistHTML = '';
  liveTasks.forEach(task => {
    tasksChecklistHTML += `
    <label style="display: flex; align-items: flex-start; gap: 8px; cursor: pointer; font-size: 0.8rem; text-align: left;">
      <input type="checkbox" class="q2-task-cb" value="${task.index}" data-title="${task.title.replace(/"/g, '&quot;')}" onchange="limitQ2Selections(this)" style="width: 18px; height: 18px; margin-top: 2px;">
      <span><strong>${task.title}:</strong> ${task.text}</span>
    </label>`;
  });

  const q2HTML = `${title}
  
  <div style="margin-top: 10px; display: flex; flex-direction: column; gap: 8px; background: rgba(255,255,255,0.03); padding: 10px; border-radius: 8px; border: 1px solid rgba(142,111,214,0.3); text-align: left;">
    ${tasksChecklistHTML}
  </div>
  
  <button onclick="submitWizardQ2()" class="btn" style="margin-top: 10px; padding: 8px 14px; font-size: 0.8rem; background: linear-gradient(135deg, var(--gold), #d4af37); color: #0C0922; font-weight: bold; width: 100%;">
    ${btnText}
  </button>`;

  appendChatMessage('assistant', q2HTML);
}'''

if old_wizard_q2_code in content:
    content = content.replace(old_wizard_q2_code, new_wizard_q2_code, 1)
    print("SUCCESS 1: Updated startWizardStep2 to parse #doable-tasks-list directly")
else:
    print("WARNING 1: Could not find old_wizard_q2_code")

# Update generateStep4AlternativeSolutions and acceptWizardAlternative to handle indexed tasks
old_step4 = '''function generateStep4AlternativeSolutions() {
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

new_step4 = '''function generateStep4AlternativeSolutions() {
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
}

function acceptWizardAlternative(btnBtn, taskIdx) {
  const altText = wizardState.generatedAlternatives[taskIdx];
  if (!altText) return;

  const container = document.getElementById('doable-tasks-list');
  if (container) {
    const cards = container.querySelectorAll('.card, [class*="card"]');
    const targetCard = cards[taskIdx];
    if (targetCard) {
      // Mark checkbox checked on Home tab
      const cb = targetCard.querySelector('input[type="checkbox"]');
      if (cb) cb.checked = true;

      // Update text description on Home tab card
      const textEl = targetCard.querySelector('p, div:nth-child(2)');
      if (textEl) textEl.innerText = altText;
    }
  }

  // Award +20 XP
  gainXP(20);

  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';

  if (btnBtn) {
    btnBtn.disabled = true;
    btnBtn.style.background = 'linear-gradient(135deg, #2ecc71, #27ae60)';
    btnBtn.style.color = '#fff';
    btnBtn.innerText = lang === 'hi' ? '✓ विकल्प संपन्न! +20 XP प्राप्त हुआ' : '✓ ALTERNATIVE COMPLETED & +20 XP CLAIMED!';
  }

  showToast(lang === 'hi' ? 'कार्य विकल्प संपन्न! +20 XP प्रदान किया गया।' : `Alternative task completed! +20 XP awarded.`);
}'''

if old_step4 in content:
    content = content.replace(old_step4, new_step4, 1)
    print("SUCCESS 2: Updated Step 4 alternative generation and DOM checkoff to target #doable-tasks-list cards directly")
else:
    print("WARNING 2: Could not find old_step4")

with open('index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print("File written.")
