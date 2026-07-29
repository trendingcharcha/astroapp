with open('index.html', 'rb') as f:
    content = f.read().decode('utf-8')

old_q2_code = '''function getLiveDashboardDoableTasks() {
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
}'''

new_q2_code = '''function getLiveDashboardDoableTasks() {
  const container = document.getElementById('quests-list-container');
  const tasks = [];

  if (container) {
    const cards = container.querySelectorAll('.quest-card, [id$="-card"], div[id^="q-"]');
    cards.forEach((card, idx) => {
      const titleEl = card.querySelector('strong, h4, [class*="title"]');
      const textEl = card.querySelector('div[id$="-text"], p, div:nth-child(2)');

      let title = titleEl ? titleEl.innerText.trim() : `Task ${idx + 1}`;
      let text = textEl ? textEl.innerText.trim() : card.innerText.trim();

      if (text.includes(title)) {
        text = text.replace(title, '').trim();
      }
      text = text.replace(/\\+\\d+\\s*XP/gi, '').trim();

      if (text.length > 95) {
        text = text.substring(0, 95) + '...';
      }

      if (title && text) {
        tasks.push({ index: idx, id: card.id || `task_${idx}`, title: title, text: text });
      }
    });
  }

  // Backup fallback: parse individual quest cards if container loop empty
  if (tasks.length === 0) {
    const categories = ['vedic', 'lalkitab', 'vastu', 'practical'];
    categories.forEach((cat, idx) => {
      const card = document.getElementById(`q-${cat}-card`);
      const textEl = document.getElementById(`q-${cat}-text`);
      if (textEl && textEl.innerText.trim()) {
        const titleEl = card ? card.querySelector('strong') : null;
        const title = titleEl ? titleEl.innerText.trim() : `${cat.toUpperCase()} Remedy`;
        let text = textEl.innerText.trim();
        if (text.length > 95) text = text.substring(0, 95) + '...';
        tasks.push({ index: idx, id: `q-${cat}-card`, title: title, text: text });
      }
    });
  }

  return tasks;
}'''

if old_q2_code in content:
    content = content.replace(old_q2_code, new_q2_code, 1)
    print("SUCCESS 1: Updated getLiveDashboardDoableTasks to parse #quests-list-container")
else:
    print("WARNING 1: Could not find old_q2_code")

# Update acceptWizardAlternative to check #quests-list-container
old_accept_code = '''function acceptWizardAlternative(btnBtn, taskIdx) {
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

new_accept_code = '''function acceptWizardAlternative(btnBtn, taskIdx) {
  const altText = wizardState.generatedAlternatives[taskIdx];
  if (!altText) return;

  const container = document.getElementById('quests-list-container');
  if (container) {
    const cards = container.querySelectorAll('.quest-card, [id$="-card"], div[id^="q-"]');
    const targetCard = cards[taskIdx];
    if (targetCard) {
      // Mark checkbox checked on Home tab
      const cb = targetCard.querySelector('input[type="checkbox"]');
      if (cb) {
        cb.checked = true;
        if (typeof gainXP === 'function') gainXP(20);
      }

      // Update text description on Home tab card
      const textEl = targetCard.querySelector('div[id$="-text"], p, div:nth-child(2)');
      if (textEl) textEl.innerText = altText;
    }
  }

  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';

  if (btnBtn) {
    btnBtn.disabled = true;
    btnBtn.style.background = 'linear-gradient(135deg, #2ecc71, #27ae60)';
    btnBtn.style.color = '#fff';
    btnBtn.innerText = lang === 'hi' ? '✓ विकल्प संपन्न! +20 XP प्राप्त हुआ' : '✓ ALTERNATIVE COMPLETED & +20 XP CLAIMED!';
  }

  showToast(lang === 'hi' ? 'कार्य विकल्प संपन्न! +20 XP प्रदान किया गया।' : `Alternative task completed! +20 XP awarded.`);
}'''

if old_accept_code in content:
    content = content.replace(old_accept_code, new_accept_code, 1)
    print("SUCCESS 2: Updated acceptWizardAlternative to target #quests-list-container")
else:
    print("WARNING 2: Could not find old_accept_code")

with open('index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print("File written.")
