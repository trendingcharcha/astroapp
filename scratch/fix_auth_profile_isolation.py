import re

file_path = r"c:\Users\EARTH\OneDrive\Desktop\Antigravity 2026\Astro AI app\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add purgeLocalUserProfileCache function right above restoreProfileFromCloud
purge_func = '''
function purgeLocalUserProfileCache() {
  const profileKeys = [
    'user_name', 'kundli_name', 'user_gender', 'kundli_gender',
    'user_dob', 'kundli_date', 'user_tob', 'kundli_time',
    'user_pob', 'kundli_city', 'user_lat', 'user_lng', 'user_timezone',
    'user_goal', 'onboarding_path', 'partner_gender', 'property_number',
    'property_type', 'property_city', 'user_streak', 'user_xp', 'user_level',
    'user_moon_rashi_idx', 'karma_daily_roadmap_history', 'karma_plan_start_date',
    'today_mission_date', 'today_quest_vedic_text', 'today_quest_lalkitab_text',
    'today_quest_vastu_text', 'today_quest_practical_text', 'user_active_goals',
    'onboarding_custom_issue', 'user_custom_issue', 'supabase_user_id'
  ];
  profileKeys.forEach(k => localStorage.removeItem(k));
  xp = 0;
  level = 1;
  streak = 0;
}

async function restoreProfileFromCloud(userId) {'''

content = content.replace("async function restoreProfileFromCloud(userId) {", purge_func, 1)

# 2. Update setupSupabaseAuthListener logic to strictly enforce account isolation
old_listener = '''supabaseClient.auth.onAuthStateChange((event, session) => {
if ((event === 'SIGNED_IN') && session && !_authListenerFired) {
_authListenerFired = true;
localStorage.setItem('user_authenticated', 'true');
localStorage.setItem('user_auth_provider', session.user?.app_metadata?.provider || 'google');
if (session.user && session.user.email) {
localStorage.setItem('user_email', session.user.email);
}

const splash = document.getElementById('splash-screen');
if (splash) splash.style.display = 'none';

const onboardingScreen = document.getElementById('onboarding-screen');
const appLayout = document.getElementById('app-layout');
const hasLocalCache = !!(localStorage.getItem('user_name') && localStorage.getItem('user_dob'));
restoreProfileFromCloud(session.user.id).then((restored) => {
// Sync local guest profile cache to cloud if logged in but no profile exists in cloud DB yet
if (!restored && hasLocalCache) {
syncProfileToCloud()
.then(() => console.log("Successfully synced local guest profile to cloud after login."))
.catch(err => console.error("Post-login background sync error:", err));
}

const appVisible = appLayout && (appLayout.style.display === 'block' || appLayout.style.display === 'flex');
if (!appVisible) {
if (restored || hasLocalCache) {
// Profile EXISTS in Supabase DB OR local cache exists → go to dashboard always
openAppDashboard();
} else {
// No profile row in DB AND no local cache → genuinely new user → onboarding
if (onboardingScreen) onboardingScreen.style.display = 'flex';
if (appLayout) appLayout.style.display = 'none';
showOnboardingStep('select-path');
}
} else {
// Logged in from settings: refresh client view to show cloud restored/synced profile
if (restored && typeof initApp === 'function') {
initApp();
}
}
}).catch((err) => {'''

new_listener = '''supabaseClient.auth.onAuthStateChange((event, session) => {
if ((event === 'SIGNED_IN') && session && !_authListenerFired) {
_authListenerFired = true;
localStorage.setItem('user_authenticated', 'true');
localStorage.setItem('user_auth_provider', session.user?.app_metadata?.provider || 'google');
if (session.user && session.user.email) {
localStorage.setItem('user_email', session.user.email);
}

// Account Isolation: Check if a different user logged in
const lastUserId = localStorage.getItem('supabase_user_id');
const currentUserId = session.user ? session.user.id : null;
let isDifferentUser = false;
if (currentUserId) {
  if (lastUserId && lastUserId !== currentUserId) {
    console.log("Different user detected! Purging previous user's local cache...");
    purgeLocalUserProfileCache();
    isDifferentUser = true;
  }
  localStorage.setItem('supabase_user_id', currentUserId);
}

const splash = document.getElementById('splash-screen');
if (splash) splash.style.display = 'none';

const onboardingScreen = document.getElementById('onboarding-screen');
const appLayout = document.getElementById('app-layout');
const hasGuestCache = !isDifferentUser && !!(localStorage.getItem('user_name') && localStorage.getItem('user_dob'));

restoreProfileFromCloud(session.user.id).then((restored) => {
// Only sync local guest cache if the user was genuinely completing a guest onboarding flow
if (!restored && hasGuestCache) {
syncProfileToCloud()
.then(() => console.log("Successfully synced local guest profile to cloud after login."))
.catch(err => console.error("Post-login background sync error:", err));
}

const appVisible = appLayout && (appLayout.style.display === 'block' || appLayout.style.display === 'flex');
if (restored) {
// Profile EXISTS in Supabase DB for THIS user -> restore and open dashboard
if (!appVisible) openAppDashboard();
else if (typeof initApp === 'function') initApp();
} else if (hasGuestCache) {
// Guest user just authenticated after filling guest info -> open dashboard
if (!appVisible) openAppDashboard();
} else {
// BRAND NEW USER with no cloud profile -> purge stale local cache & show onboarding screen
purgeLocalUserProfileCache();
localStorage.setItem('supabase_user_id', currentUserId);
if (appLayout) appLayout.style.display = 'none';
if (onboardingScreen) onboardingScreen.style.display = 'flex';
showOnboardingStep('select-path');
}
}).catch((err) => {'''

if old_listener in content:
    content = content.replace(old_listener, new_listener)
    print("SUCCESS: Replaced auth state change listener logic!")
else:
    print("WARNING: Could not find exact old_listener string. Checking snippet...")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
