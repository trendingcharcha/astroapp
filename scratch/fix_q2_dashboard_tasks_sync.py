with open('index.html', 'rb') as f:
    content = f.read().decode('utf-8')

old_step2_fn = '''function startWizardStep2() {
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
}'''

new_step2_fn = '''function getCleanShortTaskText(cat) {
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

if old_step2_fn in content:
    content = content.replace(old_step2_fn, new_step2_fn, 1)
    print("SUCCESS: Updated startWizardStep2 to extract clean 1-line tasks directly from Home Dashboard DOM")
else:
    print("WARNING: Could not find old_step2_fn")

with open('index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print("File written.")
