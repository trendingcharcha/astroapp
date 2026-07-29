with open('index.html', 'rb') as f:
    content = f.read()

# ─────────────────────────────────────────────────────────────────
# FIX 1: openLiveChatModal → pre-render today's dynamic tasks
# before Q2 tries to read them, so Karma Assistant works from ANY tab
# ─────────────────────────────────────────────────────────────────
old_open = (
    b"function openLiveChatModal() {\r\n"
    b"  const modal = document.getElementById('livechat-modal');\r\n"
    b"  if (!modal) return;\r\n"
    b"  modal.style.display = 'flex';\r\n"
    b"  \r\n"
    b"  // Reset wizard state and start Q1 flow\r\n"
    b"  wizardState = { q1_issue: '', q2_selected_tasks: [], q3_location: '', generatedAlternatives: {} };\r\n"
    b"  const msgContainer = document.getElementById('livechat-messages');\r\n"
    b"  if (msgContainer) {\r\n"
    b"    msgContainer.innerHTML = '';\r\n"
    b"    startWizardStep1();\r\n"
    b"  }\r\n"
    b"}"
)

new_open = (
    b"function openLiveChatModal() {\r\n"
    b"  const modal = document.getElementById('livechat-modal');\r\n"
    b"  if (!modal) return;\r\n"
    b"  modal.style.display = 'flex';\r\n"
    b"\r\n"
    b"  // DYNAMIC FIX: Always ensure today's live task cards are fully rendered\r\n"
    b"  // before Q2 reads them, regardless of which tab the user came from.\r\n"
    b"  const todayDay = (typeof getPlanStartDayOffset === 'function') ? getPlanStartDayOffset() : 1;\r\n"
    b"  if (typeof generateDailyQuestCards === 'function') {\r\n"
    b"    generateDailyQuestCards(todayDay);\r\n"
    b"  }\r\n"
    b"\r\n"
    b"  // Reset wizard state and start Q1 flow\r\n"
    b"  wizardState = { q1_issue: '', q2_selected_tasks: [], q3_location: '', generatedAlternatives: {} };\r\n"
    b"  const msgContainer = document.getElementById('livechat-messages');\r\n"
    b"  if (msgContainer) {\r\n"
    b"    msgContainer.innerHTML = '';\r\n"
    b"    startWizardStep1();\r\n"
    b"  }\r\n"
    b"}"
)

if old_open in content:
    content = content.replace(old_open, new_open, 1)
    print("SUCCESS 1: openLiveChatModal now pre-renders today's dynamic task cards before Q2 reads them")
else:
    print("WARNING 1: Could not find openLiveChatModal old body")

# ─────────────────────────────────────────────────────────────────
# FIX 2: getLiveDashboardDoableTasks → target [id^="task-card-"]
# dynamic cards ONLY — zero dependency on static HTML shells
# ─────────────────────────────────────────────────────────────────
old_getlive = (
    b"function getLiveDashboardDoableTasks() {\r\n"
    b"  const container = document.getElementById('quests-list-container');\r\n"
    b"  const tasks = [];\r\n"
    b"\r\n"
    b"  if (container) {\r\n"
    b"    const cards = container.querySelectorAll('.quest-card, [id$=\"-card\"], div[id^=\"q-\"]');\r\n"
    b"    cards.forEach((card, idx) => {\r\n"
    b"      const titleEl = card.querySelector('strong, h4, [class*=\"title\"]');\r\n"
    b"      const textEl = card.querySelector('div[id$=\"-text\"], p, div:nth-child(2)');\r\n"
    b"\r\n"
    b"      let title = titleEl ? titleEl.innerText.trim() : `Task ${idx + 1}`;\r\n"
    b"      let text = textEl ? textEl.innerText.trim() : card.innerText.trim();\r\n"
    b"\r\n"
    b"      if (text.includes(title)) {\r\n"
    b"        text = text.replace(title, '').trim();\r\n"
    b"      }\r\n"
    b"      text = text.replace(/\\+\\d+\\s*XP/gi, '').trim();\r\n"
    b"\r\n"
    b"      if (text.length > 95) {\r\n"
    b"        text = text.substring(0, 95) + '...';\r\n"
    b"      }\r\n"
    b"\r\n"
    b"      if (title && text) {\r\n"
    b"        tasks.push({ index: idx, id: card.id || `task_${idx}`, title: title, text: text });\r\n"
    b"      }\r\n"
    b"    });\r\n"
    b"  }\r\n"
    b"\r\n"
    b"  // Backup fallback: parse individual quest cards if container loop empty\r\n"
    b"  if (tasks.length === 0) {\r\n"
    b"    const categories = ['vedic', 'lalkitab', 'vastu', 'practical'];\r\n"
    b"    categories.forEach((cat, idx) => {\r\n"
    b"      const card = document.getElementById(`q-${cat}-card`);\r\n"
    b"      const textEl = document.getElementById(`q-${cat}-text`);\r\n"
    b"      if (textEl && textEl.innerText.trim()) {\r\n"
    b"        const titleEl = card ? card.querySelector('strong') : null;\r\n"
    b"        const title = titleEl ? titleEl.innerText.trim() : `${cat.toUpperCase()} Remedy`;\r\n"
    b"        let text = textEl.innerText.trim();\r\n"
    b"        if (text.length > 95) text = text.substring(0, 95) + '...';\r\n"
    b"        tasks.push({ index: idx, id: `q-${cat}-card`, title: title, text: text });\r\n"
    b"      }\r\n"
    b"    });\r\n"
    b"  }\r\n"
    b"\r\n"
    b"  return tasks;\r\n"
    b"}"
)

new_getlive = (
    b"function getLiveDashboardDoableTasks() {\r\n"
    b"  const container = document.getElementById('quests-list-container');\r\n"
    b"  const tasks = [];\r\n"
    b"\r\n"
    b"  if (container) {\r\n"
    b"    // DYNAMIC FIX: Target ONLY dynamically-generated task cards [id^=\"task-card-\"]\r\n"
    b"    // These are rendered fresh every day by generateDailyQuestCards(dayNum).\r\n"
    b"    // Never target static HTML shell cards (q-vedic-card etc.) which are always empty.\r\n"
    b"    const cards = container.querySelectorAll('[id^=\"task-card-\"]');\r\n"
    b"\r\n"
    b"    cards.forEach((card, idx) => {\r\n"
    b"      const titleEl = card.querySelector('strong span, strong');\r\n"
    b"      const textEl = card.querySelector('div[style*=\"text-muted\"], div:last-child');\r\n"
    b"\r\n"
    b"      let title = titleEl ? titleEl.innerText.trim() : `Task ${idx + 1}`;\r\n"
    b"      let text = textEl ? textEl.innerText.trim() : '';\r\n"
    b"\r\n"
    b"      // Strip XP badge text\r\n"
    b"      text = text.replace(/\\+\\d+\\s*XP/gi, '').trim();\r\n"
    b"      title = title.replace(/\\+\\d+\\s*XP/gi, '').trim();\r\n"
    b"\r\n"
    b"      if (text.length > 95) text = text.substring(0, 95) + '...';\r\n"
    b"\r\n"
    b"      if (title) {\r\n"
    b"        tasks.push({ index: idx, id: card.id, title: title, text: text || title });\r\n"
    b"      }\r\n"
    b"    });\r\n"
    b"  }\r\n"
    b"\r\n"
    b"  return tasks;\r\n"
    b"}"
)

if old_getlive in content:
    content = content.replace(old_getlive, new_getlive, 1)
    print("SUCCESS 2: getLiveDashboardDoableTasks now targets [id^='task-card-'] dynamic cards exclusively")
else:
    print("WARNING 2: Could not find old getLiveDashboardDoableTasks body")

# ─────────────────────────────────────────────────────────────────
# FIX 3: acceptWizardAlternative → target dynamic card by ID directly
# using task-card-{dayNum}-{taskIdx} — zero dependency on cards[] array
# ─────────────────────────────────────────────────────────────────
old_accept = (
    b"function acceptWizardAlternative(btnBtn, taskIdx) {\r\n"
    b"  const altText = wizardState.generatedAlternatives[taskIdx];\r\n"
    b"  if (!altText) return;\r\n"
    b"\r\n"
    b"  const container = document.getElementById('quests-list-container');\r\n"
    b"  if (container) {\r\n"
    b"    const cards = container.querySelectorAll('.quest-card, [id$=\"-card\"], div[id^=\"q-\"]');\r\n"
    b"    const targetCard = cards[taskIdx];\r\n"
    b"    if (targetCard) {\r\n"
    b"      // Mark checkbox checked on Home tab\r\n"
    b"      const cb = targetCard.querySelector('input[type=\"checkbox\"]');\r\n"
    b"      if (cb) {\r\n"
    b"        cb.checked = true;\r\n"
    b"        if (typeof gainXP === 'function') gainXP(20);\r\n"
    b"      }\r\n"
    b"\r\n"
    b"      // Update text description on Home tab card\r\n"
    b"      const textEl = targetCard.querySelector('div[id$=\"-text\"], p, div:nth-child(2)');\r\n"
    b"      if (textEl) textEl.innerText = altText;\r\n"
    b"    }\r\n"
    b"  }\r\n"
    b"\r\n"
    b"  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';\r\n"
    b"\r\n"
    b"  if (btnBtn) {\r\n"
    b"    btnBtn.disabled = true;\r\n"
    b"    btnBtn.style.background = 'linear-gradient(135deg, #2ecc71, #27ae60)';\r\n"
    b"    btnBtn.style.color = '#fff';\r\n"
    b"    btnBtn.innerText = lang === 'hi' ? '\u2713 \u0935\u093f\u0915\u0932\u094d\u092a \u0938\u0902\u092a\u0928\u094d\u0928! +20 XP \u092a\u094d\u0930\u093e\u092a\u094d\u0924 \u0939\u0941\u0906' : '\u2713 ALTERNATIVE COMPLETED & +20 XP CLAIMED!';\r\n"
    b"  }\r\n"
    b"\r\n"
    b"  showToast(lang === 'hi' ? '\u0915\u093e\u0930\u094d\u092f \u0935\u093f\u0915\u0932\u094d\u092a \u0938\u0902\u092a\u0928\u094d\u0928! +20 XP \u092a\u094d\u0930\u0926\u093e\u0928 \u0915\u093f\u092f\u093e \u0917\u092f\u093e\u0964' : `Alternative task completed! +20 XP awarded.`);\r\n"
    b"}"
)

new_accept = (
    b"function acceptWizardAlternative(btnBtn, taskIdx) {\r\n"
    b"  const altText = wizardState.generatedAlternatives[taskIdx];\r\n"
    b"  if (!altText) return;\r\n"
    b"\r\n"
    b"  const lang = (typeof currentAppLang !== 'undefined') ? currentAppLang : 'en';\r\n"
    b"\r\n"
    b"  // DYNAMIC FIX: Target the exact dynamically-generated task card by its ID.\r\n"
    b"  // task-card-{dayNum}-{taskIdx} is set by generateDailyQuestCards(dayNum).\r\n"
    b"  // This works for ANY task index (1st, 2nd, 5th, 7th etc.) on ANY day.\r\n"
    b"  const todayDay = (typeof getPlanStartDayOffset === 'function') ? getPlanStartDayOffset() : 1;\r\n"
    b"  const targetCard = document.getElementById(`task-card-${todayDay}-${taskIdx}`);\r\n"
    b"\r\n"
    b"  let alreadyDone = false;\r\n"
    b"  if (targetCard) {\r\n"
    b"    // Mark checkbox checked on Home tab (double-reward guard)\r\n"
    b"    const cb = targetCard.querySelector('input[type=\"checkbox\"]');\r\n"
    b"    if (cb) {\r\n"
    b"      alreadyDone = cb.checked;\r\n"
    b"      cb.checked = true;\r\n"
    b"      // Trigger visual completed state\r\n"
    b"      targetCard.classList.add('completed');\r\n"
    b"    }\r\n"
    b"\r\n"
    b"    // Update text description on Home tab card with alternative remedy text\r\n"
    b"    const textEl = targetCard.querySelector('div[style*=\"text-muted\"], div:last-child');\r\n"
    b"    if (textEl) textEl.innerText = altText;\r\n"
    b"  }\r\n"
    b"\r\n"
    b"  // Award +20 XP (double-reward protection: only if not already done)\r\n"
    b"  if (!alreadyDone && typeof gainXP === 'function') {\r\n"
    b"    gainXP(20);\r\n"
    b"  }\r\n"
    b"\r\n"
    b"  // Persist alternative completion to roadmap history for today\r\n"
    b"  try {\r\n"
    b"    const todayDay2 = (typeof getPlanStartDayOffset === 'function') ? getPlanStartDayOffset() : 1;\r\n"
    b"    const hist = JSON.parse(localStorage.getItem('karma_daily_roadmap_history') || '{}');\r\n"
    b"    if (!hist[todayDay2]) hist[todayDay2] = {};\r\n"
    b"    hist[todayDay2][taskIdx] = true;\r\n"
    b"    localStorage.setItem('karma_daily_roadmap_history', JSON.stringify(hist));\r\n"
    b"  } catch(e) {}\r\n"
    b"\r\n"
    b"  if (btnBtn) {\r\n"
    b"    btnBtn.disabled = true;\r\n"
    b"    btnBtn.style.background = 'linear-gradient(135deg, #2ecc71, #27ae60)';\r\n"
    b"    btnBtn.style.color = '#fff';\r\n"
    b"    btnBtn.innerText = lang === 'hi' ? '\u2713 \u0935\u093f\u0915\u0932\u094d\u092a \u0938\u0902\u092a\u0928\u094d\u0928! +20 XP \u092a\u094d\u0930\u093e\u092a\u094d\u0924 \u0939\u0941\u0906' : '\u2713 ALTERNATIVE COMPLETED & +20 XP CLAIMED!';\r\n"
    b"  }\r\n"
    b"\r\n"
    b"  showToast(lang === 'hi' ? '\u0915\u093e\u0930\u094d\u092f \u0935\u093f\u0915\u0932\u094d\u092a \u0938\u0902\u092a\u0928\u094d\u0928! +20 XP \u092a\u094d\u0930\u0926\u093e\u0928 \u0915\u093f\u092f\u093e \u0917\u092f\u093e\u0964' : `Alternative task completed! +20 XP awarded.`);\r\n"
    b"}"
)

if old_accept in content:
    content = content.replace(old_accept, new_accept, 1)
    print("SUCCESS 3: acceptWizardAlternative now targets task-card-{day}-{taskIdx} dynamically with double-reward protection")
else:
    print("WARNING 3: Could not find old acceptWizardAlternative body")

# Bump cache version
content = content.replace(
    b"var APP_CACHE_VER = 'cv_20260728_TOTAL_GLOBAL_PURGE_v1020';",
    b"var APP_CACHE_VER = 'cv_20260728_TOTAL_GLOBAL_PURGE_v1025';"
)

with open('index.html', 'wb') as f:
    f.write(content)

print("SUCCESS: Cache version bumped to v1025")
print("File written.")
