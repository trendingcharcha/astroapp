import re

with open('index.html', 'rb') as f:
    content = f.read().decode('utf-8')

# 1. Add Feedback & Live Chat buttons in Settings tab (below LOG OUT button)
old_logout_btn = '<button onclick="handleLogout()" class="btn" style="background: #381414; color: #ff6b6b; box-shadow: none;"><span class="k-lbl-en">LOG OUT</span><span class="k-lbl-hi" style="display:none;">लॉग आउट</span></button>'

new_settings_buttons = '''<button onclick="handleLogout()" class="btn" style="background: #381414; color: #ff6b6b; box-shadow: none;"><span class="k-lbl-en">LOG OUT</span><span class="k-lbl-hi" style="display:none;">लॉग आउट</span></button>

<div style="margin-top: 15px; display: flex; flex-direction: column; gap: 10px;">
  <!-- MANDATORY FEEDBACK & RATING BUTTON -->
  <button onclick="openFeedbackModal()" class="btn" style="background: rgba(232, 200, 121, 0.15); border: 1px solid var(--gold); color: var(--gold); box-shadow: 0 4px 15px rgba(232,200,121,0.15);">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle; margin-right:8px;"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
    <span class="k-lbl-en">APP FEEDBACK & RATING</span><span class="k-lbl-hi" style="display:none;">ऐप प्रतिक्रिया एवं रेटिंग</span>
  </button>

  <!-- LIVE AI KARMA ASSISTANT CHAT BUTTON -->
  <button onclick="openLiveChatModal()" class="btn" style="background: rgba(142, 111, 214, 0.18); border: 1px solid var(--purple); color: var(--purple); box-shadow: 0 4px 15px rgba(142,111,214,0.2);">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle; margin-right:8px;"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><line x1="9" y1="9" x2="15" y2="9"/><line x1="9" y1="13" x2="13" y2="13"/></svg>
    <span class="k-lbl-en">LIVE AI ASSISTANT CHAT (TASK ADAPTER)</span><span class="k-lbl-hi" style="display:none;">लाइव एआई सहचर चैट (अनुकूलन)</span>
  </button>
</div>'''

if old_logout_btn in content:
    content = content.replace(old_logout_btn, new_settings_buttons, 1)
    print("SUCCESS 1: Added Feedback & Live Chat buttons to Settings tab")
else:
    print("WARNING 1: Could not find old_logout_btn")

# 2. Add Feedback & Live Chat HTML Modals + JS logic before </body>
modals_and_js = '''
<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- 1. MANDATORY FEEDBACK & STAR RATING MODAL OVERLAY -->
<!-- ═══════════════════════════════════════════════════════════════ -->
<div id="feedback-modal" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(12, 9, 34, 0.92); backdrop-filter: blur(10px); z-index: 100005; align-items: center; justify-content: center; padding: 20px;">
  <div class="auth-card" style="max-width: 440px; width: 100%; border: 1px solid var(--gold); box-shadow: 0 15px 40px rgba(0,0,0,0.8); max-height: 90vh; overflow-y: auto;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid rgba(232, 200, 121, 0.2); padding-bottom: 10px;">
      <h3 style="color: var(--gold); margin: 0; font-size: 1.1rem; display: flex; align-items: center; gap: 8px;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
        <span class="k-lbl-en">App Feedback & Rating</span>
        <span class="k-lbl-hi" style="display:none;">ऐप प्रतिक्रिया एवं रेटिंग</span>
      </h3>
      <button class="btn" style="width: auto; padding: 4px 10px; font-size: 0.8rem; background: rgba(255,255,255,0.05);" onclick="closeFeedbackModal()">✕</button>
    </div>

    <form onsubmit="submitFeedback(event)">
      <!-- FULL NAME (MANDATORY) -->
      <div class="form-group">
        <label><span class="k-lbl-en">Full Name *</span><span class="k-lbl-hi" style="display:none;">पूरा नाम *</span></label>
        <input type="text" id="fb-name" required placeholder="Enter your full name">
      </div>

      <!-- EMAIL ADDRESS (MANDATORY) -->
      <div class="form-group">
        <label><span class="k-lbl-en">Email Address *</span><span class="k-lbl-hi" style="display:none;">ईमेल पता *</span></label>
        <input type="email" id="fb-email" required placeholder="your.email@example.com">
      </div>

      <!-- PHONE NUMBER (MANDATORY) -->
      <div class="form-group">
        <label><span class="k-lbl-en">Phone Number *</span><span class="k-lbl-hi" style="display:none;">फ़ोन नंबर *</span></label>
        <input type="tel" id="fb-phone" required placeholder="+91 XXXXX XXXXX">
      </div>

      <!-- OCCUPATION / PROFESSION (MANDATORY) -->
      <div class="form-group">
        <label><span class="k-lbl-en">Occupation / Profession *</span><span class="k-lbl-hi" style="display:none;">व्यवसाय / पेशा *</span></label>
        <input type="text" id="fb-profession" required placeholder="e.g. Software Engineer, Doctor, Student, Business">
      </div>

      <!-- STAR RATING (MANDATORY) -->
      <div class="form-group" style="text-align: center; background: rgba(255,255,255,0.03); border: 1px dashed rgba(232,200,121,0.3); border-radius: 12px; padding: 12px; margin-bottom: 15px;">
        <label style="display: block; margin-bottom: 8px; font-weight: bold; color: var(--gold);">
          <span class="k-lbl-en">Star Rating *</span><span class="k-lbl-hi" style="display:none;">स्टार रेटिंग *</span>
        </label>
        <div id="fb-star-container" style="display: flex; justify-content: center; gap: 8px; font-size: 1.6rem; cursor: pointer;">
          <svg onclick="selectStarRating(1)" class="fb-star-icon" id="fb-star-1" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
          <svg onclick="selectStarRating(2)" class="fb-star-icon" id="fb-star-2" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
          <svg onclick="selectStarRating(3)" class="fb-star-icon" id="fb-star-3" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
          <svg onclick="selectStarRating(4)" class="fb-star-icon" id="fb-star-4" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
          <svg onclick="selectStarRating(5)" class="fb-star-icon" id="fb-star-5" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
        </div>
        <p id="fb-star-label" style="font-size: 0.78rem; color: var(--gold); margin: 6px 0 0 0; font-weight: 500;">Select rating (1 to 5 Stars)</p>
      </div>

      <!-- FEEDBACK COMMENTS (OPTIONAL) -->
      <div class="form-group">
        <label><span class="k-lbl-en">Feedback / Suggestions (Optional)</span><span class="k-lbl-hi" style="display:none;">प्रतिक्रिया / सुझाव (वैकल्पिक)</span></label>
        <textarea id="fb-comments" rows="3" placeholder="Share your experience or suggestions to help us improve..."></textarea>
      </div>

      <button type="submit" id="fb-submit-btn" class="btn" style="width: 100%; margin-top: 10px;">
        <span class="k-lbl-en">SUBMIT FEEDBACK</span><span class="k-lbl-hi" style="display:none;">प्रतिक्रिया भेजें</span>
      </button>
    </form>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════ -->
<!-- 2. LIVE AI KARMA ASSISTANT CHAT MODAL OVERLAY -->
<!-- ═══════════════════════════════════════════════════════════════ -->
<div id="livechat-modal" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(12, 9, 34, 0.95); backdrop-filter: blur(12px); z-index: 100010; align-items: center; justify-content: center; padding: 15px;">
  <div class="auth-card" style="max-width: 480px; width: 100%; height: 85vh; border: 1px solid var(--purple); box-shadow: 0 15px 40px rgba(0,0,0,0.9); display: flex; flex-direction: column; padding: 0; overflow: hidden; border-radius: 16px;">
    
    <!-- Chat Header -->
    <div style="background: linear-gradient(135deg, rgba(142, 111, 214, 0.25), rgba(12, 9, 34, 0.8)); padding: 14px 18px; border-bottom: 1px solid rgba(142, 111, 214, 0.3); display: flex; justify-content: space-between; align-items: center;">
      <div style="display: flex; align-items: center; gap: 10px;">
        <div style="width: 38px; height: 38px; border-radius: 50%; background: linear-gradient(135deg, var(--purple), var(--gold)); display: flex; align-items: center; justify-content: center; box-shadow: 0 0 10px rgba(142, 111, 214, 0.5);">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><path d="M12 2a10 10 0 0 1 10 10c0 5.52-4.48 10-10 10a9.94 9.94 0 0 1-5-1.34L2 22l1.34-5A9.94 9.94 0 0 1 2 12C2 6.48 6.48 2 12 2z"/></svg>
        </div>
        <div>
          <h4 style="margin: 0; color: #fff; font-size: 0.95rem; font-weight: bold;">
            <span class="k-lbl-en">AI Karma Assistant</span><span class="k-lbl-hi" style="display:none;">एआई कर्म सहचर</span>
          </h4>
          <p id="chat-header-sub" style="margin: 0; color: var(--gold); font-size: 0.72rem;">Personalized Task Adapter & Guidance</p>
        </div>
      </div>
      <button class="btn" style="width: auto; padding: 4px 10px; font-size: 0.8rem; background: rgba(255,255,255,0.1);" onclick="closeLiveChatModal()">✕</button>
    </div>

    <!-- Quick Scenario Prompts Carousel -->
    <div style="background: rgba(255,255,255,0.02); padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; gap: 8px; overflow-x: auto; white-space: nowrap;">
      <button onclick="sendQuickPrompt('office')" class="btn btn-outline" style="padding: 4px 10px; font-size: 0.72rem; border-color: rgba(142,111,214,0.4); color: var(--purple);">🏢 In Office Right Now</button>
      <button onclick="sendQuickPrompt('time')" class="btn btn-outline" style="padding: 4px 10px; font-size: 0.72rem; border-color: rgba(232,200,121,0.4); color: var(--gold);">⏰ Missed Time Window</button>
      <button onclick="sendQuickPrompt('items')" class="btn btn-outline" style="padding: 4px 10px; font-size: 0.72rem; border-color: rgba(255,255,255,0.3); color: #fff;">🏠 Don't Have Items</button>
      <button onclick="sendQuickPrompt('desk')" class="btn btn-outline" style="padding: 4px 10px; font-size: 0.72rem; border-color: rgba(46,204,113,0.4); color: #2ecc71;">🧘 Quick Desk Remedy</button>
    </div>

    <!-- Messages Container -->
    <div id="livechat-messages" style="flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; background: rgba(10,8,28,0.6);">
      <!-- Messages rendered dynamically -->
    </div>

    <!-- Chat Input Form -->
    <form onsubmit="handleLiveChatSubmit(event)" style="padding: 10px 14px; background: rgba(18, 13, 43, 0.95); border-top: 1px solid rgba(142, 111, 214, 0.2); display: flex; gap: 8px;">
      <input type="text" id="livechat-input" required placeholder="Tell Assistant your situation (e.g. at office, traveling)..." style="flex: 1; font-size: 0.85rem; padding: 10px 12px; border-radius: 8px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.15); color: #fff;">
      <button type="submit" class="btn" style="width: auto; padding: 10px 16px; font-size: 0.85rem; background: linear-gradient(135deg, var(--purple), #6c5ce7);">
        <span class="k-lbl-en">SEND</span><span class="k-lbl-hi" style="display:none;">भेजें</span>
      </button>
    </form>

  </div>
</div>

<script>
// ═══════════════════════════════════════════════════════════════
// FEEDBACK & LIVE CHAT ENGINE IMPLEMENTATION
// ═══════════════════════════════════════════════════════════════
let selectedStarRating = 0;

function openFeedbackModal() {
  const modal = document.getElementById('feedback-modal');
  if (!modal) return;
  
  // Auto-fill existing profile details
  const nameEl = document.getElementById('fb-name');
  const emailEl = document.getElementById('fb-email');
  const phoneEl = document.getElementById('fb-phone');
  const profEl = document.getElementById('fb-profession');
  
  if (nameEl) nameEl.value = localStorage.getItem('user_name') || localStorage.getItem('kundli_name') || '';
  if (emailEl) emailEl.value = localStorage.getItem('user_email') || '';
  if (phoneEl) phoneEl.value = localStorage.getItem('user_phone') || '';
  if (profEl) {
    const storedProf = localStorage.getItem('user_profession') || (document.getElementById('c-profession') ? document.getElementById('c-profession').value : '');
    profEl.value = storedProf || '';
  }
  
  modal.style.display = 'flex';
}

function closeFeedbackModal() {
  const modal = document.getElementById('feedback-modal');
  if (modal) modal.style.display = 'none';
}

function selectStarRating(rating) {
  selectedStarRating = rating;
  for (let i = 1; i <= 5; i++) {
    const star = document.getElementById('fb-star-' + i);
    if (star) {
      if (i <= rating) {
        star.setAttribute('fill', 'var(--gold)');
        star.setAttribute('stroke', 'var(--gold)');
      } else {
        star.setAttribute('fill', 'none');
        star.setAttribute('stroke', 'var(--gold)');
      }
    }
  }
  const label = document.getElementById('fb-star-label');
  if (label) {
    const descriptions = ['', '1 Star - Needs Improvement', '2 Stars - Fair', '3 Stars - Good', '4 Stars - Very Good', '5 Stars - Excellent Cosmic Experience!'];
    label.innerText = descriptions[rating] || (rating + ' Stars Selected');
  }
}

async function submitFeedback(e) {
  e.preventDefault();
  if (selectedStarRating < 1) {
    showToast(currentAppLang === 'hi' ? 'कृपया कम से कम 1 स्टार रेटिंग चुनें!' : 'Please select a star rating (1 to 5 stars)!');
    return;
  }

  const name = document.getElementById('fb-name').value.trim();
  const email = document.getElementById('fb-email').value.trim();
  const phone = document.getElementById('fb-phone').value.trim();
  const profession = document.getElementById('fb-profession').value.trim();
  const comments = document.getElementById('fb-comments') ? document.getElementById('fb-comments').value.trim() : '';

  const btn = document.getElementById('fb-submit-btn');
  if (btn) {
    btn.disabled = true;
    btn.innerText = currentAppLang === 'hi' ? 'जमा हो रहा है...' : 'Submitting...';
  }

  // Save phone number locally for session profile completeness
  localStorage.setItem('user_phone', phone);
  localStorage.setItem('user_profession', profession);

  const feedbackPayload = {
    full_name: name,
    email: email,
    phone: phone,
    profession: profession,
    rating: selectedStarRating,
    comments: comments,
    created_at: new Date().toISOString()
  };

  // 1. Submit to Supabase Cloud Database table 'feedbacks'
  let cloudSuccess = false;
  if (typeof supabaseClient !== 'undefined' && supabaseClient && supabaseClient.from) {
    try {
      const { error } = await supabaseClient.from('feedbacks').insert([feedbackPayload]);
      if (!error) {
        cloudSuccess = true;
        console.log('[Feedback] Successfully inserted to Supabase feedbacks table');
      } else {
        console.warn('[Feedback] Supabase insert note:', error.message);
      }
    } catch (err) {
      console.error('[Feedback] Supabase catch:', err);
    }
  }

  // 2. Save local backup to ensure data is never lost
  const localHistory = JSON.parse(localStorage.getItem('user_feedback_history') || '[]');
  localHistory.push(feedbackPayload);
  localStorage.setItem('user_feedback_history', JSON.stringify(localHistory));

  if (btn) {
    btn.disabled = false;
    btn.innerHTML = '<span class="k-lbl-en">SUBMIT FEEDBACK</span><span class="k-lbl-hi" style="display:none;">प्रतिक्रिया भेजें</span>';
  }

  closeFeedbackModal();
  showToast(currentAppLang === 'hi' ? 'आपकी प्रतिक्रिया सफलतापूर्वक दर्ज कर ली गई है! धन्यवाद।' : 'Thank you! Your feedback and rating have been recorded.');
}

// ═══════════════════════════════════════════════════════════════
// LIVE AI ASSISTANT CHAT & TASK ADAPTER
// ═══════════════════════════════════════════════════════════════
let pendingAlternativeTask = null;

function openLiveChatModal() {
  const modal = document.getElementById('livechat-modal');
  if (!modal) return;
  
  modal.style.display = 'flex';
  const msgContainer = document.getElementById('livechat-messages');
  if (msgContainer && msgContainer.children.length === 0) {
    // Initial welcome message from AI Karma Assistant
    const name = localStorage.getItem('user_name') || 'Seeker';
    const goal = localStorage.getItem('user_goal') || 'job';
    const initialMsg = `Namaste <strong>${name}</strong>! I am your AI Karma Assistant.<br><br>I see your active goal is <strong>${goal.toUpperCase()}</strong>. If you are busy at office, traveling, or miss a specific time window, tell me here. I will dynamically generate a valid alternative task tailored for your situation that you can accept right away!`;
    appendChatMessage('assistant', initialMsg);
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
  msgDiv.style.maxWidth = '85%';
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

function sendQuickPrompt(type) {
  const prompts = {
    office: "I am in office right now and can't perform tasks requiring water/food offering. What is my desk alternative?",
    time: "I missed the morning Brahma/Rahu Kaal time window. How can I perform today's remedy now?",
    items: "I don't have copper coins or silver items at home today. What alternative item can I use?",
    desk: "Suggest a quick 2-minute office desk remedy for today."
  };
  const text = prompts[type] || prompts.office;
  document.getElementById('livechat-input').value = text;
  handleLiveChatSubmit(new Event('submit'));
}

function handleLiveChatSubmit(e) {
  if (e) e.preventDefault();
  const inputEl = document.getElementById('livechat-input');
  if (!inputEl) return;
  const userText = inputEl.value.trim();
  if (!userText) return;

  appendChatMessage('user', userText);
  inputEl.value = '';

  // Generate dynamic contextual AI response & alternative task
  setTimeout(() => {
    generateAIAdaptationResponse(userText);
  }, 400);
}

function generateAIAdaptationResponse(query) {
  const userName = localStorage.getItem('user_name') || 'Seeker';
  const goal = localStorage.getItem('user_goal') || 'job';
  const qLower = query.toLowerCase();

  let responseHTML = '';
  let alternativeTaskText = '';

  if (qLower.includes('office') || qLower.includes('desk') || qLower.includes('work')) {
    alternativeTaskText = "Desk Chant: Mentally repeat 'Om Namah Shivaya' 11x while facing East at your desk";
    responseHTML = `No problem, <strong>${userName}</strong>! We never force rigid constraints. Since you are at your office desk, here is your valid office alternative:<br><br>
    <strong>Alternative Remedy:</strong> Sit upright at your desk facing East, take 3 deep breaths, and mentally chant <em>'Om Namah Shivaya' 11 times</em> to harmonize your Lagna energy.`;
  } else if (qLower.includes('time') || qLower.includes('missed') || qLower.includes('rahu')) {
    alternativeTaskText = "Time Adapter: Offer 1 glass of clean drinking water to a colleague or drink mindfully facing North";
    responseHTML = `Missing a time window is completely fine, <strong>${userName}</strong>! Astrological remedies can be adapted to evening sunset hours:<br><br>
    <strong>Alternative Remedy:</strong> Drink a glass of clean water facing North, or offer water to a colleague at work with a positive intention for your <strong>${goal.toUpperCase()}</strong> goal.`;
  } else if (qLower.includes('item') || qLower.includes('coin') || qLower.includes('silver')) {
    alternativeTaskText = "No-Item Remedy: Touch green plant leaf or write your goal 3x in a notebook";
    responseHTML = `You don't need physical coins or items to activate planetary grace, <strong>${userName}</strong>!<br><br>
    <strong>Alternative Remedy:</strong> Touch a green leaf of any indoor plant, or write your goal 3 times in your personal notepad.`;
  } else {
    alternativeTaskText = "Desk Adaption: Take 5 conscious Sattvic breaths facing East at your desk";
    responseHTML = `Understood, <strong>${userName}</strong>! Here is your custom Sattvic alternative for your <strong>${goal.toUpperCase()}</strong> goal:<br><br>
    <strong>Alternative Remedy:</strong> Pause for 2 minutes, close your eyes, and take 5 conscious breaths while visualizing success in your target goal.`;
  }

  pendingAlternativeTask = alternativeTaskText;

  responseHTML += `<div style="margin-top: 10px; background: rgba(232, 200, 121, 0.1); border: 1px dashed var(--gold); border-radius: 8px; padding: 10px; text-align: center;">
    <p style="margin: 0 0 6px 0; font-size: 0.75rem; color: var(--gold); font-weight: bold;">PROPOSED ALTERNATIVE TASK:</p>
    <p style="margin: 0 0 10px 0; font-size: 0.8rem; color: #fff;">"${alternativeTaskText}"</p>
    <button onclick="acceptAlternativeTask()" class="btn" style="width: 100%; padding: 6px 12px; font-size: 0.78rem; background: linear-gradient(135deg, var(--gold), #d4af37); color: #0C0922; font-weight: bold;">
      ✓ ACCEPT & UPDATE TODAY'S TASK
    </button>
  </div>`;

  appendChatMessage('assistant', responseHTML);
}

function acceptAlternativeTask() {
  if (!pendingAlternativeTask) return;

  // Replace today's active vedic quest text with accepted alternative
  localStorage.setItem('today_quest_vedic_text', pendingAlternativeTask);
  localStorage.setItem('today_quest_vedic_text_en', pendingAlternativeTask);
  localStorage.setItem('today_quest_vedic_text_hi', pendingAlternativeTask);

  // Update DOM elements on Home tab
  const questEl = document.getElementById('q-vedic-text');
  if (questEl) questEl.innerText = pendingAlternativeTask;

  appendChatMessage('assistant', `✓ <strong>Alternative Task Accepted!</strong><br>Your active daily task has been updated on your Home Dashboard to:<br><em>"${pendingAlternativeTask}"</em><br><br>You can now complete it and check it off on your Home tab to claim your full XP!`);

  showToast(currentAppLang === 'hi' ? 'दैनिक कार्य नया स्वीकार्य विकल्प के साथ अपडेट हो गया है!' : "Daily task updated to accepted alternative! Check it off on your Home tab.");
}
</script>
'''

if '</body>' in content:
    content = content.replace('</body>', modals_and_js + '\n</body>', 1)
    print("SUCCESS 2: Added Feedback & Live Chat Modals + JavaScript engine before </body>")
else:
    print("WARNING 2: Could not find </body> tag")

with open('index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print("File written.")
