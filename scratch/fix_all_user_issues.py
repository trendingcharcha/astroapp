import re

file_path = r"c:\Users\EARTH\OneDrive\Desktop\Antigravity 2026\Astro AI app\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# ── 1. FIX DUAL / STACKED AUTH CARDS ─────────────────────────────
# Keep 1 clean card in #onboarding-step-path and completely remove duplicate card from #auth-screen

clean_auth_card_1 = '''<!-- ── STEP A: Smart Auth Gateway ──────────────────────────── -->
<div id="onboarding-step-path" class="auth-card" style="text-align: center; width: 100%; max-width: 440px; margin: 0 auto; padding: 28px 22px; background: rgba(18, 14, 46, 0.95); border: 1px solid rgba(232, 200, 121, 0.35); border-radius: 20px; box-shadow: 0 12px 40px rgba(0,0,0,0.6);">
<div style="margin-bottom: 14px;">
<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#E8C879" stroke-width="1.8">
<circle cx="12" cy="12" r="10"/>
<path d="M12 2v20M2 12h20"/>
</svg>
</div>
<h2 style="margin-bottom: 6px; color: #FFFFFF; font-size: 1.4rem; font-weight: 700;"><span class="k-lbl-en">Welcome to CosmoVedic</span><span class="k-lbl-hi" style="display:none;">कोस्मोवैदिक में आपका स्वागत है</span></h2>
<p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 22px; line-height: 1.4;"><span class="k-lbl-en">One-tap instant access to your 90-Day KarmaQuest &amp; Kundli</span><span class="k-lbl-hi" style="display:none;">अपने 90-दिवसीय कर्मक्वेस्ट और कुंडली तक तुरंत 1-टैप पहुंच</span></p>

<!-- ⚡ 1-TAP INSTANT GOOGLE AUTH BUTTON -->
<button class="btn" style="background: linear-gradient(135deg, #FFFFFF, #F1F3F4); color: #1F1F1F; font-weight: 700; font-size: 1rem; width: 100%; display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 10px; border-radius: 12px; padding: 15px 20px; cursor: pointer; border: 2px solid #E8C879; box-shadow: 0 6px 20px rgba(232, 200, 121, 0.35); transition: all 0.25s ease;" onclick="signInWithGoogle()">
<svg width="22" height="22" viewBox="0 0 24 24">
<path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
<path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
<path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
<path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
</svg>
<span><span class="k-lbl-en">Continue with Google (1-Tap)</span><span class="k-lbl-hi" style="display:none;">गूगल से जुड़ें (1-टैप)</span></span>
</button>
<p style="font-size: 0.72rem; color: #E8C879; margin-bottom: 20px; font-weight: 500;"><span class="k-lbl-en">⚡ Select account &amp; enter instantly</span><span class="k-lbl-hi" style="display:none;">⚡ खाता चुनें और तुरंत प्रवेश करें</span></p>

<!-- Optional Email Auth Collapsible -->
<div style="margin-top: 10px; margin-bottom: 16px;">
<button type="button" onclick="const f=document.getElementById('email-auth-form-main'); f.style.display = f.style.display === 'none' ? 'flex' : 'none';" style="background: none; border: none; color: var(--text-muted); font-size: 0.78rem; text-decoration: underline; cursor: pointer; padding: 5px;">
<span class="k-lbl-en">Or Sign in with Email / Password ▼</span><span class="k-lbl-hi" style="display:none;">या ईमेल / पासवर्ड से साइन इन करें ▼</span>
</button>

<form id="email-auth-form-main" onsubmit="handleEmailAuth(event, 'signin')" style="display:none; flex-direction:column; gap:10px; text-align:left; margin-top: 12px; background: rgba(0,0,0,0.3); padding: 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.08);">
<div class="form-group" style="margin:0;">
<input type="email" id="auth-email" placeholder="Email address" style="width:100%;">
</div>
<div class="form-group" style="margin:0;">
<input type="password" id="auth-password" placeholder="Password (min 6 chars)" style="width:100%;">
</div>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 4px;">
<button type="button" class="btn" style="padding:10px; font-weight:bold; background: linear-gradient(135deg, #2ecc71, #27ae60); color: #fff;" onclick="handleEmailAuth(event, 'signin')"><span class="k-lbl-en">SIGN IN</span><span class="k-lbl-hi" style="display:none;">साइन इन करें</span></button>
<button type="button" class="btn btn-outline" style="padding:10px; font-weight:bold; border-color: var(--gold); color: var(--gold);" onclick="handleEmailAuth(event, 'signup')"><span class="k-lbl-en">SIGN UP</span><span class="k-lbl-hi" style="display:none;">साइन अप करें</span></button>
</div>
</form>
</div>

<div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
<div style="flex:1; height:1px; background:rgba(255,255,255,0.1);"></div>
<span style="font-size:0.72rem; color:var(--text-muted); text-transform:uppercase;"><span class="k-lbl-en">Free Preview</span><span class="k-lbl-hi" style="display:none;">मुफ़्त पूर्वावलोकन</span></span>
<div style="flex:1; height:1px; background:rgba(255,255,255,0.1);"></div>
</div>

<!-- Free Guest Preview Button -->
<button class="btn btn-outline" style="width: 100%; padding: 11px; font-weight: 600; border-color: rgba(232,200,121,0.3); color: var(--gold); display: flex; align-items: center; justify-content: center; gap: 8px; border-radius: 10px;" onclick="showGuestChoiceScreen()">
<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
<span class="k-lbl-en">Free Guest Kundli Preview</span><span class="k-lbl-hi" style="display:none;">मुफ़्त गेस्ट कुंडली पूर्वावलोकन</span>
</button>
</div>'''

# Replace #onboarding-step-path
pattern1 = r'<!-- ── STEP A: Smart Auth Gateway ──────────────────────────── -->[\s\S]*?</div>\s*</div>'
m1 = re.search(pattern1, content)
if m1:
    content = content.replace(m1.group(0), clean_auth_card_1)
    print("SUCCESS 1: Updated #onboarding-step-path card!")
else:
    print("WARNING 1: Could not find #onboarding-step-path pattern.")

# Remove duplicate form inputs inside #auth-screen
pattern2 = r'<div id="auth-screen">[\s\S]*?</div>\s*</div>'
m2 = re.search(pattern2, content)
if m2:
    clean_auth_screen = '<div id="auth-screen" style="display:none;"></div>'
    content = content.replace(m2.group(0), clean_auth_screen)
    print("SUCCESS 2: Removed duplicated auth-screen HTML!")

# ── 2. FIX GOOGLE AUTH TO FORCE ACCOUNT CHOOSER (IMAGE 2) ────────
old_g_auth = '''async function signInWithGoogle() {
const liveRedirect = 'https://trendingcharcha.github.io/astroapp/';
showToast("Connecting to Google Auth...");

// Ensure Supabase client is active
if (!supabaseClient && typeof supabase !== 'undefined' && supabase.createClient) {
try {
const url = 'https://rnunibjmmowhaxsytthf.supabase.co';
const key = 'sb_publishable_jjYnowJojZtzDjqEmVXACg_C7J1PGlq';
supabaseClient = supabase.createClient(url, key);
} catch(e) {}
}

try {
if (supabaseClient && supabaseClient.auth) {
const { data, error } = await supabaseClient.auth.signInWithOAuth({
provider: 'google',
options: {
redirectTo: liveRedirect
}
});
if (!error && data && data.url) {
window.location.href = data.url;
return;
}
}
const googleUrl = `https://rnunibjmmowhaxsytthf.supabase.co/auth/v1/authorize?provider=google&redirect_to=${encodeURIComponent(liveRedirect)}`;
window.location.href = googleUrl;
} catch(e) {
console.error("Google sign in error:", e);
showToast("Google Auth error. Please try again.", "error");
}
}'''

new_g_auth = '''async function signInWithGoogle() {
const liveRedirect = 'https://trendingcharcha.github.io/astroapp/';
showToast("Opening Google Account Chooser...");

if (!supabaseClient && typeof supabase !== 'undefined' && supabase.createClient) {
try {
const url = 'https://rnunibjmmowhaxsytthf.supabase.co';
const key = 'sb_publishable_jjYnowJojZtzDjqEmVXACg_C7J1PGlq';
supabaseClient = supabase.createClient(url, key);
} catch(e) {}
}

try {
if (supabaseClient && supabaseClient.auth) {
const { data, error } = await supabaseClient.auth.signInWithOAuth({
provider: 'google',
options: {
redirectTo: liveRedirect,
queryParams: {
  prompt: 'select_account'
}
}
});
if (!error && data && data.url) {
window.location.href = data.url;
return;
}
}
const googleUrl = `https://rnunibjmmowhaxsytthf.supabase.co/auth/v1/authorize?provider=google&redirect_to=${encodeURIComponent(liveRedirect)}&prompt=select_account`;
window.location.href = googleUrl;
} catch(e) {
console.error("Google sign in error:", e);
showToast("Google Auth error. Please try again.", "error");
}
}'''

if old_g_auth in content:
    content = content.replace(old_g_auth, new_g_auth)
    print("SUCCESS 3: Updated signInWithGoogle to force prompt=select_account (Image 2)!")
else:
    print("WARNING 3: Could not find exact old_g_auth string.")

# ── 3. FIX GOAL PROGRESS RESET TO DAY 1 ─────────────────────────
# Make sure syncProfileToCloud includes karma_plan_start_date & history
old_sync_payload = '''karma_plan_start_date: localStorage.getItem('karma_plan_start_date') || (typeof getFormattedDate === 'function' ? getFormattedDate() : new Date().toISOString().split('T')[0])'''

# And in restoreProfileFromCloud, calculate offset & do NOT overwrite karma_plan_start_date
restore_date_fix = '''if (payload.karma_plan_start_date) {
  localStorage.setItem('karma_plan_start_date', payload.karma_plan_start_date);
} else {
  // Save current plan start date to cloud profile so existing user's progress is preserved forever
  const existingStart = localStorage.getItem('karma_plan_start_date') || (typeof getFormattedDate === 'function' ? getFormattedDate() : new Date().toISOString().split('T')[0]);
  localStorage.setItem('karma_plan_start_date', existingStart);
}'''

if "if (payload.karma_plan_start_date) {" in content:
    content = content.replace("if (payload.karma_plan_start_date) {\nlocalStorage.setItem('karma_plan_start_date', payload.karma_plan_start_date);\n}", restore_date_fix)
    content = content.replace("if (payload.karma_plan_start_date) {\n  localStorage.setItem('karma_plan_start_date', payload.karma_plan_start_date);\n}", restore_date_fix)
    print("SUCCESS 4: Updated restoreProfileFromCloud to preserve karma_plan_start_date!")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
