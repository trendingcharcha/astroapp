with open('index.html', 'rb') as f:
    content = f.read().decode('utf-8')

# Fix startWizardStep1, handleWizardQ1, startWizardStep3, handleWizardQ3 to use integer indices
old_step1 = '''function startWizardStep1() {
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
}'''

new_step1 = '''function startWizardStep1() {
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
    <button onclick="handleWizardQ1(this, 1)" class="btn btn-outline" style="text-align: left !important; justify-content: flex-start !important; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff; width: 100%; display: flex; align-items: center;">${btn1}</button>
    <button onclick="handleWizardQ1(this, 2)" class="btn btn-outline" style="text-align: left !important; justify-content: flex-start !important; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff; width: 100%; display: flex; align-items: center;">${btn2}</button>
    <button onclick="handleWizardQ1(this, 3)" class="btn btn-outline" style="text-align: left !important; justify-content: flex-start !important; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff; width: 100%; display: flex; align-items: center;">${btn3}</button>
    <button onclick="handleWizardQ1(this, 4)" class="btn btn-outline" style="text-align: left !important; justify-content: flex-start !important; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff; width: 100%; display: flex; align-items: center;">${btn4}</button>
  </div>`;
  
  appendChatMessage('assistant', q1HTML);
}

function handleWizardQ1(btn, index) {
  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';
  const optionsEn = [
    "",
    "1️⃣ I skipped today's selective task",
    "2️⃣ I am unable to perform the selective task today",
    "3️⃣ I was in a hurry and forgot my morning tasks",
    "4️⃣ I do not have the required task items"
  ];
  const optionsHi = [
    "",
    "1️⃣ मैंने आज का विशेष कार्य छोड़ दिया",
    "2️⃣ मैं आज विशेष कार्य करने में असमर्थ हूँ",
    "3️⃣ मैं जल्दी में था/थी और सुबह का कार्य भूल गया/गई",
    "4️⃣ मेरे पास आवश्यक सामग्री उपलब्ध नहीं है"
  ];
  
  const issueText = lang === 'hi' ? optionsHi[index] : optionsEn[index];
  wizardState.q1_issue = issueText;
  appendChatMessage('user', lang === 'hi' ? `चयनित कारण: "${issueText}"` : `Issue Selected: "${issueText}"`);
  
  setTimeout(() => {
    startWizardStep2();
  }, 300);
}'''

if old_step1 in content:
    content = content.replace(old_step1, new_step1, 1)
    print("SUCCESS 1: Updated Q1 onclick handlers to integer indices")
else:
    print("WARNING 1: Could not find old_step1, using string replace...")

# Fix Q3 onclick handlers similarly
old_step3 = '''function startWizardStep3() {
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
}'''

new_step3 = '''function startWizardStep3() {
  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';

  const title = lang === 'hi'
    ? `<strong>Q3: अभी आप कहाँ स्थित हैं?</strong><br><span style="font-size: 0.75rem; color: var(--gold);">(नीचे से 1 स्थान चुनें)</span>`
    : `<strong>Q3: Where are you located right now?</strong><br><span style="font-size: 0.75rem; color: var(--gold);">(Select 1 location below)</span>`;

  const btn1 = lang === 'hi' ? "🏠 घर पर" : "🏠 Home";
  const btn2 = lang === 'hi' ? "🏢 कार्यालय / कार्यस्थल पर" : "🏢 Office / Workplace";
  const btn3 = lang === 'hi' ? "🚗 बाहर बाजार में / यात्रा में" : "🚗 Outside in Market / Traveling";

  const q3HTML = `${title}
  
  <div style="margin-top: 10px; display: flex; flex-direction: column; gap: 8px; align-items: flex-start; text-align: left;">
    <button onclick="handleWizardQ3(this, 1)" class="btn btn-outline" style="text-align: left !important; justify-content: flex-start !important; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff; width: 100%; display: flex; align-items: center;">${btn1}</button>
    <button onclick="handleWizardQ3(this, 2)" class="btn btn-outline" style="text-align: left !important; justify-content: flex-start !important; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff; width: 100%; display: flex; align-items: center;">${btn2}</button>
    <button onclick="handleWizardQ3(this, 3)" class="btn btn-outline" style="text-align: left !important; justify-content: flex-start !important; padding: 8px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.4); color: #fff; width: 100%; display: flex; align-items: center;">${btn3}</button>
  </div>`;

  appendChatMessage('assistant', q3HTML);
}

function handleWizardQ3(btn, index) {
  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';
  const locsEn = ["", "Home", "Office", "Outside in Market / Traveling"];
  const locsHi = ["", "घर पर", "कार्यालय / कार्यस्थल पर", "बाहर बाजार में / यात्रा में"];
  
  const locationText = lang === 'hi' ? locsHi[index] : locsEn[index];
  wizardState.q3_location = locationText;
  appendChatMessage('user', lang === 'hi' ? `स्थान: "${locationText}"` : `Location: "${locationText}"`);

  setTimeout(() => {
    generateStep4AlternativeSolutions();
  }, 400);
}'''

if old_step3 in content:
    content = content.replace(old_step3, new_step3, 1)
    print("SUCCESS 2: Updated Q3 onclick handlers to integer indices")
else:
    print("WARNING 2: Could not find old_step3")

with open('index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print("File written.")
