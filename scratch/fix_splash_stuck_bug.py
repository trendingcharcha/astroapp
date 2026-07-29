import re

file_path = r"c:\Users\EARTH\OneDrive\Desktop\Antigravity 2026\Astro AI app\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

pattern = r'// Smooth Transition Splash to Onboarding / Auth Screen[\s\S]*?setTimeout\(dismissSplashScreen, 2000\);'

clean_splash_func = '''// Smooth Transition Splash to Onboarding / Auth Screen
async function dismissSplashScreen() {
const splash = document.getElementById('splash-screen');
const onboarding = document.getElementById('onboarding-screen');
const appLayout = document.getElementById('app-layout');

// Ensure Supabase client is initialized if not yet done
if (!supabaseClient && typeof loadCloudConfig === 'function') {
try { loadCloudConfig(); } catch(e) {}
}

// Check if URL contains Google OAuth Callback tokens/code
const hash = window.location.hash;
const search = window.location.search;
const isOAuthRedirect = (hash && (hash.includes('access_token=') || hash.includes('type='))) || (search && search.includes('code='));

if (isOAuthRedirect) {
if (splash) splash.style.display = 'none';
return; // Allow handleOAuthCallback to manage screen routing!
}

if (splash) {
splash.style.opacity = '0';
splash.style.display = 'none';
}

try {
const isAuthFlag = localStorage.getItem('user_authenticated') === 'true';
const hasLocalProfile = !!(localStorage.getItem('user_name') && localStorage.getItem('user_dob'));

let validBackendUser = false;
let currentUserId = null;
if (supabaseClient && supabaseClient.auth) {
try {
const { data: { user }, error } = await supabaseClient.auth.getUser();
if (user && !error) {
validBackendUser = true;
currentUserId = user.id;
}
} catch (err) {
console.log("Supabase backend auth check error:", err);
}
}

let cloudProfileExists = false;
if (validBackendUser && currentUserId) {
try {
cloudProfileExists = await restoreProfileFromCloud(currentUserId);
} catch(e) {
cloudProfileExists = hasLocalProfile;
}
}

// If user has active auth session OR cloud profile OR local profile -> Dashboard
if (isAuthFlag || validBackendUser || cloudProfileExists || hasLocalProfile) {
if (onboarding) onboarding.style.display = 'none';
if (appLayout) appLayout.style.display = 'block';
if (typeof initApp === 'function') initApp();
} else {
// New unauthenticated guest -> Onboarding Auth gateway
if (appLayout) appLayout.style.display = 'none';
if (onboarding) onboarding.style.display = 'flex';
showOnboardingStep('path');
}
} catch(err) {
console.error('[Astro AI] Splash dismissal error:', err);
const hasLocalProfile = !!(localStorage.getItem('user_name') && localStorage.getItem('user_dob'));
if (hasLocalProfile) {
if (onboarding) onboarding.style.display = 'none';
if (appLayout) appLayout.style.display = 'block';
if (typeof initApp === 'function') initApp();
} else {
if (appLayout) appLayout.style.display = 'none';
if (onboarding) onboarding.style.display = 'flex';
showOnboardingStep('path');
}
}
}

if (document.readyState === 'loading') {
document.addEventListener('DOMContentLoaded', () => setTimeout(dismissSplashScreen, 500));
} else {
setTimeout(dismissSplashScreen, 500);
}
setTimeout(dismissSplashScreen, 1500);'''

m = re.search(pattern, content)
if m:
    content = content.replace(m.group(0), clean_splash_func)
    print("SUCCESS: Replaced dismissSplashScreen with async implementation!")
else:
    print("WARNING: Could not match dismissSplashScreen pattern.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
