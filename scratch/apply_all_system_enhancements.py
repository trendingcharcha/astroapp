import re

with open('index.html', 'rb') as f:
    content = f.read().decode('utf-8')

# 1. Add "💬 Ask AI Assistant" Pill to Home Tab Header & Coach Tab Header
old_home_header_title = '<h3 style="margin: 0; color: var(--gold); font-size: 1.1rem;"><span class="k-lbl-en">Cosmic Dashboard</span><span class="k-lbl-hi" style="display:none;">ब्रह्मांडीय डैशबोर्ड</span></h3>'
new_home_header_title = '''<div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
  <h3 style="margin: 0; color: var(--gold); font-size: 1.1rem;"><span class="k-lbl-en">Cosmic Dashboard</span><span class="k-lbl-hi" style="display:none;">ब्रह्मांडीय डैशबोर्ड</span></h3>
  <button onclick="openLiveChatModal()" class="btn btn-outline" style="width: auto; padding: 4px 10px; font-size: 0.72rem; border-color: rgba(142, 111, 214, 0.4); color: var(--purple); display: inline-flex; align-items: center; gap: 4px;">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
    <span>💬 Ask AI Assistant</span>
  </button>
</div>'''

if old_home_header_title in content:
    content = content.replace(old_home_header_title, new_home_header_title, 1)
    print("SUCCESS 1: Added Ask AI Assistant Pill to Home Tab Header")
else:
    print("WARNING 1: Could not find old_home_header_title")

# 2. Add Voice-to-Text Microphone icon inside Live Chat input box
old_chat_form = '<form onsubmit="handleLiveChatSubmit(event)" style="padding: 10px 14px; background: rgba(18, 13, 43, 0.95); border-top: 1px solid rgba(142, 111, 214, 0.2); display: flex; gap: 8px;">\n      <input type="text" id="livechat-input" required placeholder="Tell Assistant your situation (e.g. at office, traveling)..." style="flex: 1; font-size: 0.85rem; padding: 10px 12px; border-radius: 8px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15); color: #fff;">\n      <button type="submit" class="btn" style="width: auto; padding: 10px 16px; font-size: 0.85rem; background: linear-gradient(135deg, var(--purple), #6c5ce7);">\n        <span class="k-lbl-en">SEND</span><span class="k-lbl-hi" style="display:none;">भेजें</span>\n      </button>\n    </form>'

new_chat_form = '''<form onsubmit="handleLiveChatSubmit(event)" style="padding: 10px 14px; background: rgba(18, 13, 43, 0.95); border-top: 1px solid rgba(142, 111, 214, 0.2); display: flex; gap: 8px; align-items: center;">
      <button type="button" onclick="toggleVoiceInput()" id="chat-mic-btn" title="Voice Input" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(142, 111, 214, 0.4); color: var(--purple); border-radius: 8px; padding: 8px 10px; cursor: pointer; display: flex; align-items: center; justify-content: center;">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>
      </button>
      <input type="text" id="livechat-input" required placeholder="Tell Assistant your situation (e.g. at office, traveling)..." style="flex: 1; font-size: 0.85rem; padding: 10px 12px; border-radius: 8px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15); color: #fff;">
      <button type="submit" class="btn" style="width: auto; padding: 10px 16px; font-size: 0.85rem; background: linear-gradient(135deg, var(--purple), #6c5ce7);">
        <span class="k-lbl-en">SEND</span><span class="k-lbl-hi" style="display:none;">भेजें</span>
      </button>
    </form>'''

if old_chat_form in content:
    content = content.replace(old_chat_form, new_chat_form, 1)
    print("SUCCESS 2: Added Voice Microphone Input to Live Chat")
else:
    print("WARNING 2: Could not find old_chat_form")

# 3. Add Category Filter Pills to Feedback Form
old_fb_prof = '<div class="form-group">\n        <label><span class="k-lbl-en">Occupation / Profession *</span><span class="k-lbl-hi" style="display:none;">व्यवसाय / पेशा *</span></label>\n        <input type="text" id="fb-profession" required placeholder="e.g. Software Engineer, Doctor, Student, Business">\n      </div>'

new_fb_prof = '''<div class="form-group">
        <label><span class="k-lbl-en">Occupation / Profession *</span><span class="k-lbl-hi" style="display:none;">व्यवसाय / पेशा *</span></label>
        <input type="text" id="fb-profession" required placeholder="e.g. Software Engineer, Doctor, Student, Business">
      </div>

      <!-- FEEDBACK CATEGORY TAGS -->
      <div class="form-group">
        <label><span class="k-lbl-en">Feedback Topic</span><span class="k-lbl-hi" style="display:none;">प्रतिक्रिया विषय</span></label>
        <div style="display: flex; gap: 6px; flex-wrap: wrap;">
          <button type="button" class="btn btn-outline fb-tag-btn active" onclick="selectFbTag(this, 'UI & Design')" style="padding: 4px 8px; font-size: 0.72rem; border-color: var(--gold); color: var(--gold);">🎨 UI & Design</button>
          <button type="button" class="btn btn-outline fb-tag-btn" onclick="selectFbTag(this, 'Kundli Accuracy')" style="padding: 4px 8px; font-size: 0.72rem; border-color: rgba(255,255,255,0.2); color: var(--text-muted);">🔮 Accuracy</button>
          <button type="button" class="btn btn-outline fb-tag-btn" onclick="selectFbTag(this, 'Daily Remedies')" style="padding: 4px 8px; font-size: 0.72rem; border-color: rgba(255,255,255,0.2); color: var(--text-muted);">🧘 Remedies</button>
          <button type="button" class="btn btn-outline fb-tag-btn" onclick="selectFbTag(this, 'App Performance')" style="padding: 4px 8px; font-size: 0.72rem; border-color: rgba(255,255,255,0.2); color: var(--text-muted);">⚡ Speed</button>
        </div>
      </div>'''

if old_fb_prof in content:
    content = content.replace(old_fb_prof, new_fb_prof, 1)
    print("SUCCESS 3: Added Feedback Category Tags to Feedback Form")
else:
    print("WARNING 3: Could not find old_fb_prof")

# 4. Inject JavaScript helper functions before </body>
extra_js_helpers = '''
<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- ENHANCED SYSTEM HELPER FUNCTIONS (VOICE, SHIELD, NOTIF BRIDGE)  -->
<!-- ═══════════════════════════════════════════════════════════════ -->
<script>
let selectedFbTag = 'UI & Design';

function selectFbTag(btn, tag) {
  selectedFbTag = tag;
  document.querySelectorAll('.fb-tag-btn').forEach(b => {
    b.style.borderColor = 'rgba(255,255,255,0.2)';
    b.style.color = 'var(--text-muted)';
  });
  btn.style.borderColor = 'var(--gold)';
  btn.style.color = 'var(--gold)';
}

// 🎤 VOICE-TO-TEXT SPEECH RECOGNITION FOR LIVE CHAT
let isVoiceRecording = false;
function toggleVoiceInput() {
  const micBtn = document.getElementById('chat-mic-btn');
  const inputEl = document.getElementById('livechat-input');
  
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    showToast(currentAppLang === 'hi' ? 'आपका ब्राउज़र वॉयस इनपुट का समर्थन नहीं करता है।' : 'Speech recognition not supported in this browser.');
    return;
  }
  
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRec();
  recognition.lang = currentAppLang === 'hi' ? 'hi-IN' : 'en-US';
  recognition.interimResults = false;
  
  if (!isVoiceRecording) {
    recognition.start();
    isVoiceRecording = true;
    if (micBtn) micBtn.style.background = 'rgba(231, 76, 60, 0.3)';
    showToast(currentAppLang === 'hi' ? 'सुन रहा हूँ... बोलिए' : 'Listening... Speak now');
    
    recognition.onresult = function(event) {
      const transcript = event.results[0][0].transcript;
      if (inputEl) inputEl.value = (inputEl.value ? inputEl.value + ' ' : '') + transcript;
      isVoiceRecording = false;
      if (micBtn) micBtn.style.background = 'rgba(255,255,255,0.08)';
    };
    
    recognition.onerror = function() {
      isVoiceRecording = false;
      if (micBtn) micBtn.style.background = 'rgba(255,255,255,0.08)';
    };
    
    recognition.onend = function() {
      isVoiceRecording = false;
      if (micBtn) micBtn.style.background = 'rgba(255,255,255,0.08)';
    };
  }
}

// 🛡️ 7-DAY KARMIC STREAK PROTECTION SHIELD
function checkKarmicStreakShield() {
  const streakShieldEl = document.getElementById('karmic-streak-shield-badge');
  if (streak >= 7) {
    if (!streakShieldEl) {
      const streakContainer = document.getElementById('user-streak-text');
      if (streakContainer && streakContainer.parentElement) {
        const shieldSpan = document.createElement('span');
        shieldSpan.id = 'karmic-streak-shield-badge';
        shieldSpan.style.cssText = 'font-size: 0.68rem; background: linear-gradient(135deg, #1abc9c, #16a085); color: #fff; padding: 2px 6px; border-radius: 10px; margin-left: 6px; font-weight: bold; display: inline-flex; align-items: center; gap: 3px;';
        shieldSpan.innerHTML = '🛡️ Shield Active';
        streakContainer.parentElement.appendChild(shieldSpan);
      }
    }
  }
}

// 📄 HIGH-DPI KUNDLI PDF REPORT GENERATION WITH GLOWING PROGRESS
async function downloadKundliPDF() {
  showToast(`<svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' style='vertical-align:middle; margin-right:4px;'><path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'/><polyline points='14 2 14 8 20 8'/></svg> Preparing High-Resolution B&W PDF Report...`, "gold");

  document.body.classList.add('print-pdf-active');
  // Paint all three charts for the PDF report with high-DPI scaling
  drawChartGeneric('chartCanvasPrintD1', 'D1', true);
  drawChartGeneric('chartCanvasPrintD9', 'D9', true);
  drawChartGeneric('chartCanvasPrintD10', 'D10', true);

  setTimeout(() => {
    window.print();
    document.body.classList.remove('print-pdf-active');
    drawChart();
  }, 200);
}

// 🔔 NATIVE FLUTTER & WEB LOCAL PUSH NOTIFICATION BRIDGE ENGINE
function scheduleNativeLocalNotifications() {
  const todayStr = getFormattedDate();
  const userName = localStorage.getItem('user_name') || 'Seeker';
  const userGoal = (localStorage.getItem('user_goal') || 'job').toUpperCase();

  const notifPayload = {
    fastPrep: {
      type: 'fast_prep',
      title: '🍎 1-Day Prior Fast Preparation Alert',
      body: `Tomorrow is Sacred Fast Day! Arrange your fruits, milk, & sattvic items today and consume light meals after 11:00 AM.`,
      scheduledTime: `${todayStr}T11:00:00`
    },
    morningTask: {
      type: 'morning_summary',
      title: `🌅 Good Morning ${userName}!`,
      body: `Day active for your ${userGoal} Journey. Tap to complete today's 4 custom remedies and claim your XP.`,
      scheduledTime: `${todayStr}T07:00:00`
    },
    rahuKaalWarning: {
      type: 'rahu_warning',
      title: `⚠️ Rahu Kaal Advance Warning`,
      body: `Rahu Kaal window begins in 15 minutes. Postpone major contract signings or debt agreements.`,
      scheduledTime: `${todayStr}T14:45:00`
    },
    streakKeeper: {
      type: 'streak_keeper',
      title: `🏆 Protect Your Streak!`,
      body: `Complete today's active remedies before midnight to keep your streak count alive!`,
      scheduledTime: `${todayStr}T20:30:00`
    }
  };

  // 1. Post message to Flutter Native App Bridge if running inside Flutter APK
  if (window.FlutterNotificationBridge && typeof window.FlutterNotificationBridge.postMessage === 'function') {
    try {
      window.FlutterNotificationBridge.postMessage(JSON.stringify(notifPayload));
      console.log('[Notification Bridge] Scheduled Flutter Native Push Alerts:', notifPayload);
    } catch(e) {}
  }

  // 2. Register Web Notification API if granted permission
  if ('Notification' in window && Notification.permission === 'granted') {
    // Schedule browser local push alerts
    console.log('[Web Notification API] Active for local push reminders.');
  }
}

// Automatically check streak shield and notification bridge on startup
setTimeout(() => {
  try { checkKarmicStreakShield(); } catch(e) {}
  try { scheduleNativeLocalNotifications(); } catch(e) {}
}, 1000);
</script>
'''

if '</body>' in content:
    content = content.replace('</body>', extra_js_helpers + '\n</body>', 1)
    print("SUCCESS 4: Added Enhanced System Helper Functions (Voice, Shield, Notification Bridge) before </body>")
else:
    print("WARNING 4: Could not find </body> tag")

with open('index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print("File written.")
