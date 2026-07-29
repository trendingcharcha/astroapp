file_path = r"c:\Users\EARTH\OneDrive\Desktop\Antigravity 2026\Astro AI app\index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_code = '''if (_hasCloudProfile || (localStorage.getItem('user_name') && localStorage.getItem('user_dob'))) {
showToast(`<svg width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' style='vertical-align:middle; margin-right:4px;'><path d='M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m11.314 11.314l.707-.707'/></svg> Welcome back! Loading your dashboard...`);
openAppDashboard();
} else {
showToast(`<svg width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' style='vertical-align:middle; margin-right:4px;'><path d='M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m11.314 11.314l.707-.707'/></svg> Welcome! Please complete your profile.`);
const onboarding = document.getElementById('onboarding-screen');
const appLayout = document.getElementById('app-layout');
if (appLayout) appLayout.style.display = 'none';
if (onboarding) onboarding.style.display = 'flex';
showOnboardingStep('select-path');
}'''

new_code = '''if (_hasCloudProfile) {
showToast(`<svg width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' style='vertical-align:middle; margin-right:4px;'><path d='M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m11.314 11.314l.707-.707'/></svg> Welcome back! Loading your profile...`);
openAppDashboard();
} else {
// New user with no cloud profile -> purge old local cache & force onboarding
purgeLocalUserProfileCache();
if (userId) localStorage.setItem('supabase_user_id', userId);
showToast(`<svg width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' style='vertical-align:middle; margin-right:4px;'><path d='M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m11.314 11.314l.707-.707'/></svg> Welcome! Please complete your profile.`);
const onboarding = document.getElementById('onboarding-screen');
const appLayout = document.getElementById('app-layout');
if (appLayout) appLayout.style.display = 'none';
if (onboarding) onboarding.style.display = 'flex';
showOnboardingStep('select-path');
}'''

if old_code in content:
    content = content.replace(old_code, new_code)
    print("SUCCESS: Updated handleEmailAuth profile check!")
else:
    print("WARNING: Could not find exact handleEmailAuth snippet.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
