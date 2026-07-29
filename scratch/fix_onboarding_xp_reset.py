with open('index.html', 'rb') as f:
    content = f.read()

old_onboarding_storage = (
    "localStorage.setItem('user_goal', goal);\r\n"
    "localStorage.setItem('user_active_goals', JSON.stringify([goal]));\r\n"
    "localStorage.setItem('onboarding_path', onboardingPath || 'single');"
).encode('utf-8')

new_onboarding_storage = (
    "localStorage.setItem('user_goal', goal);\r\n"
    "localStorage.setItem('user_active_goals', JSON.stringify([goal]));\r\n"
    "localStorage.setItem('onboarding_path', onboardingPath || 'single');\r\n"
    "\r\n"
    "// Reset XP and level to fresh starting state on Day 1 onboarding submit\r\n"
    "xp = 0;\r\n"
    "level = 1;\r\n"
    "localStorage.setItem('user_xp', '0');\r\n"
    "localStorage.setItem('user_level', '1');\r\n"
    "if (typeof updateGamificationHeader === 'function') updateGamificationHeader();"
).encode('utf-8')

if old_onboarding_storage in content:
    content = content.replace(old_onboarding_storage, new_onboarding_storage, 1)
    print("SUCCESS: Added XP reset to 0 in submitOnboarding()")
else:
    print("WARNING: Could not find old_onboarding_storage")

with open('index.html', 'wb') as f:
    f.write(content)

print("File written.")
