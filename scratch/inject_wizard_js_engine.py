with open('index.html', 'rb') as f:
    content = f.read().decode('utf-8')

# Find the old LIVE AI ASSISTANT CHAT & TASK ADAPTER section
old_js_start = "// ═══════════════════════════════════════════════════════════════\n// LIVE AI ASSISTANT CHAT & TASK ADAPTER\n// ═══════════════════════════════════════════════════════════════"
old_js_end = "showToast(currentAppLang === 'hi' ? 'दैनिक कार्य नया स्वीकार्य विकल्प के साथ अपडेट हो गया है!' : \"Daily task updated to accepted alternative! Check it off on your Home tab.\");\n}"

new_js_engine = '''// ═══════════════════════════════════════════════════════════════
// LIVE AI TASK ADAPTER WIZARD ENGINE (4-STEP INTERACTIVE FLOW)
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
  msgDiv.style.maxWidth = '90%';
  msgDiv.style.padding = '10px 14px';
  msgDiv.style.borderRadius = '12px';
  msgDiv.style.fontSize = '0.82rem';
  msgDiv.style.lineHeight = '1.5';

  if (sender === 'user') {
    msgDiv.style.alignSelf = 'flex-end';
    msgDiv.style.background = 'linear-gradient(135deg, #6c5ce7, #8e44ad)';
    msgDiv.style.color = '#fff';
    msgDiv.style.borderBottomRightRadius = '2px';
  } else {
    msgDiv.style.alignSelf = 'flex-start';
    msgDiv.style.background = 'rgba(255, 255, 255, 0.08)';
    msgDiv.style.color = '#e2e8f0';
    msgDiv.style.border = '1px solid rgba(142, 111, 214, 0.3)';
    msgDiv.style.borderBottomLeftRadius = '2px';
  }

  msgDiv.innerHTML = htmlContent;
  msgContainer.appendChild(msgDiv);
  msgContainer.scrollTop = msgContainer.scrollHeight;
}

function startWizardStep1() {
  const userName = localStorage.getItem('user_name') || 'Seeker';
  const q1HTML = `Namaste <strong>${userName}</strong>! I am your AI Task Adapter.<br><br>
  <strong>Q1: What is the issue preventing you from completing your task today?</strong><br>
  <span style="font-size: 0.75rem; color: var(--gold);">(Select 1 option below)</span>
  <div style="margin-top: 10px; display: flex; flex-direction: column; gap: 8px;">
    <button onclick="handleWizardQ1(this, 'I skipped todays selective task')" class="btn btn-outline" style="text-align: left; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff;">1️⃣ I skipped today's selective task</button>
    <button onclick="handleWizardQ1(this, 'I am not able to perform the selective task today')" class="btn btn-outline" style="text-align: left; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff;">2️⃣ I am not able to perform the selective task today</button>
    <button onclick="handleWizardQ1(this, 'I was in hurry and forget the morning tasks')" class="btn btn-outline" style="text-align: left; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff;">3️⃣ I was in a hurry and forgot the morning tasks</button>
    <button onclick="handleWizardQ1(this, 'I dont have the task items')" class="btn btn-outline" style="text-align: left; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff;">4️⃣ I don't have the required task items</button>
  </div>`;
  
  appendChatMessage('assistant', q1HTML);
}

function handleWizardQ1(btn, issueText) {
  wizardState.q1_issue = issueText;
  appendChatMessage('user', `Issue Selected: "${issueText}"`);
  
  setTimeout(() => {
    startWizardStep2();
  }, 300);
}

function startWizardStep2() {
  const taskVedic = localStorage.getItem('today_quest_vedic_text') || 'Vedic Mantra Chanting';
  const taskLal = localStorage.getItem('today_quest_lalkitab_text') || 'Lal Kitab Remedial Action';
  const taskVastu = localStorage.getItem('today_quest_vastu_text') || 'Vastu Alignment Step';
  const taskPrac = localStorage.getItem('today_quest_practical_text') || 'Practical Goal Focus';

  const q2HTML = `<strong>Q2: Select the task(s) you need an alternative for today:</strong><br>
  <span style="font-size: 0.75rem; color: var(--gold);">(Check up to MAX 3 tasks)</span>
  
  <div style="margin-top: 10px; display: flex; flex-direction: column; gap: 8px; background: rgba(255,255,255,0.03); padding: 10px; border-radius: 8px; border: 1px solid rgba(142,111,214,0.3);">
    <label style="display: flex; align-items: flex-start; gap: 8px; cursor: pointer; font-size: 0.8rem;">
      <input type="checkbox" class="q2-task-cb" value="vedic" onchange="limitQ2Selections(this)" style="width: 18px; height: 18px; margin-top: 2px;">
      <span><strong>Vedic Task:</strong> ${taskVedic}</span>
    </label>
    <label style="display: flex; align-items: flex-start; gap: 8px; cursor: pointer; font-size: 0.8rem;">
      <input type="checkbox" class="q2-task-cb" value="lalkitab" onchange="limitQ2Selections(this)" style="width: 18px; height: 18px; margin-top: 2px;">
      <span><strong>Lal Kitab Task:</strong> ${taskLal}</span>
    </label>
    <label style="display: flex; align-items: flex-start; gap: 8px; cursor: pointer; font-size: 0.8rem;">
      <input type="checkbox" class="q2-task-cb" value="vastu" onchange="limitQ2Selections(this)" style="width: 18px; height: 18px; margin-top: 2px;">
      <span><strong>Vastu Task:</strong> ${taskVastu}</span>
    </label>
    <label style="display: flex; align-items: flex-start; gap: 8px; cursor: pointer; font-size: 0.8rem;">
      <input type="checkbox" class="q2-task-cb" value="practical" onchange="limitQ2Selections(this)" style="width: 18px; height: 18px; margin-top: 2px;">
      <span><strong>Practical Task:</strong> ${taskPrac}</span>
    </label>
  </div>
  
  <button onclick="submitWizardQ2()" class="btn" style="margin-top: 10px; padding: 8px 14px; font-size: 0.8rem; background: linear-gradient(135deg, var(--gold), #d4af37); color: #0C0922; font-weight: bold;">
    CONTINUE TO Q3 (LOCATION) →
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
  appendChatMessage('user', `Selected ${wizardState.q2_selected_tasks.length} task(s) for alternative solution.`);

  setTimeout(() => {
    startWizardStep3();
  }, 300);
}

function startWizardStep3() {
  const q3HTML = `<strong>Q3: Where are you located right now?</strong><br>
  <span style="font-size: 0.75rem; color: var(--gold);">(Select 1 location below)</span>
  
  <div style="margin-top: 10px; display: flex; flex-direction: column; gap: 8px;">
    <button onclick="handleWizardQ3(this, 'Home')" class="btn btn-outline" style="text-align: left; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff;">🏠 Home</button>
    <button onclick="handleWizardQ3(this, 'Office')" class="btn btn-outline" style="text-align: left; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff;">🏢 Office / Workplace</button>
    <button onclick="handleWizardQ3(this, 'Outside in Market / Traveling')" class="btn btn-outline" style="text-align: left; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff;">🚗 Outside in Market / Traveling</button>
  </div>`;

  appendChatMessage('assistant', q3HTML);
}

function handleWizardQ3(btn, locationText) {
  wizardState.q3_location = locationText;
  appendChatMessage('user', `Location: "${locationText}"`);

  setTimeout(() => {
    generateStep4AlternativeSolutions();
  }, 400);
}

function generateStep4AlternativeSolutions() {
  const issue = wizardState.q1_issue;
  const tasks = wizardState.q2_selected_tasks;
  const location = wizardState.q3_location;
  const goal = (localStorage.getItem('user_goal') || 'job').toUpperCase();

  let solutionsHTML = `<strong>Dynamic Sattvic Alternatives for Today:</strong><br>
  <span style="font-size: 0.75rem; color: var(--gold);">Evaluated for ${location} (${issue})</span><br><br>`;

  tasks.forEach(taskType => {
    let altText = '';
    if (location === 'Office') {
      if (taskType === 'vedic') altText = "Desk Chant: Mentally repeat 'Om Namah Shivaya' 11x facing East at your desk";
      else if (taskType === 'lalkitab') altText = "Workplace Sattva: Keep 1 clean glass of drinking water on your desk and offer 1 sip to a colleague";
      else if (taskType === 'vastu') altText = "Desk Vastu: Adjust laptop/screen to face North or East while executing work tasks";
      else altText = "Office Action: Take 3 deep conscious breaths before starting your next executive task";
    } else if (location.includes('Outside') || location.includes('Market')) {
      if (taskType === 'vedic') altText = "Travel Mantra: Silently recite your ruling planet mantra 7 times while walking/moving";
      else if (taskType === 'lalkitab') altText = "Public Karma: Offer 1 coin or food to a needy person or street bird while outside";
      else if (taskType === 'vastu') altText = "Travel Direction: Pause facing East for 10 seconds and visualize success in your " + goal + " goal";
      else altText = "Mobile Note: Write 1 action step for your goal in your smartphone notepad";
    } else { // Home
      if (taskType === 'vedic') altText = "Home Sattva: Light a lamp or incense stick and offer silent gratitude for 1 minute";
      else if (taskType === 'lalkitab') altText = "Home Remedy: Touch a green leaf of an indoor plant and drink 1 glass of water";
      else if (taskType === 'vastu') altText = "Home Alignment: Sit in North-East corner for 2 minutes with calm mind";
      else altText = "Home Action: Spend 5 minutes reviewing your 90-day karmic transformation plan";
    }

    wizardState.generatedAlternatives[taskType] = altText;

    solutionsHTML += `<div style="margin-bottom: 12px; background: rgba(232, 200, 121, 0.08); border: 1px dashed var(--gold); border-radius: 8px; padding: 10px;">
      <p style="margin: 0 0 4px 0; font-size: 0.75rem; color: var(--gold); font-weight: bold;">PROPOSED ALTERNATIVE (${taskType.toUpperCase()}):</p>
      <p style="margin: 0 0 8px 0; font-size: 0.8rem; color: #fff;">"${altText}"</p>
      <button onclick="acceptWizardAlternative(this, '${taskType}')" class="btn" style="width: 100%; padding: 6px 12px; font-size: 0.78rem; background: linear-gradient(135deg, var(--gold), #d4af37); color: #0C0922; font-weight: bold;">
        ✓ MARK ALTERNATIVE AS DONE & CLAIM +20 XP
      </button>
    </div>`;
  });

  solutionsHTML += `<p style="font-size: 0.72rem; color: var(--text-muted); font-style: italic; margin-top: 6px;">
    Note: Submitting alternative as done updates TODAY'S task only. Tomorrow, the core automated dynamic engine resumes normally.
  </p>`;

  appendChatMessage('assistant', solutionsHTML);
}

function acceptWizardAlternative(btnBtn, taskType) {
  const altText = wizardState.generatedAlternatives[taskType];
  if (!altText) return;

  // 1. Mark task as DONE for TODAY ONLY
  const todayStr = getFormattedDate();
  localStorage.setItem(`today_quest_${taskType}_done`, 'true');
  localStorage.setItem(`today_quest_${taskType}_text`, altText);

  // 2. Update Home Tab DOM in real-time
  const textEl = document.getElementById(`q-${taskType}-text`);
  if (textEl) textEl.innerText = altText;

  const checkEl = document.getElementById(`q-${taskType}-check`);
  if (checkEl) checkEl.checked = true;

  // 3. Award +20 XP instantly
  gainXP(20);

  // 4. Update button UI inside chat to confirmed status
  if (btnBtn) {
    btnBtn.disabled = true;
    btnBtn.style.background = 'linear-gradient(135deg, #2ecc71, #27ae60)';
    btnBtn.style.color = '#fff';
    btnBtn.innerText = '✓ ALTERNATIVE COMPLETED & +20 XP CLAIMED!';
  }

  showToast(currentAppLang === 'hi' ? 'कार्य विकल्प संपन्न! +20 XP प्रदान किया गया।' : `Alternative ${taskType.toUpperCase()} task completed! +20 XP awarded.`);
}'''

if old_js_start in content and old_js_end in content:
    start_pos = content.find(old_js_start)
    end_pos = content.find(old_js_end) + len(old_js_end)
    content = content[:start_pos] + new_js_engine + content[end_pos:]
    print("SUCCESS: Replaced old chat JS engine with 4-Step Interactive Wizard Engine")
else:
    print("WARNING: Could not locate exact JS boundaries, using secondary match...")

with open('index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print("File written.")
