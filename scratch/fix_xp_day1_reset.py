with open('index.html', 'rb') as f:
    content = f.read()

# 1. Reset user_xp to 0 upon fresh onboarding submit
old_submit_xp_reset = (
    "localStorage.setItem('user_goal', selectedGoal);\r\n"
    "localStorage.setItem('onboarding_path', onboardingPath);"
).encode('utf-8')

new_submit_xp_reset = (
    "localStorage.setItem('user_goal', selectedGoal);\r\n"
    "localStorage.setItem('onboarding_path', onboardingPath);\r\n"
    "// Reset XP to 0 for fresh Day 1 onboarding start\r\n"
    "xp = 0;\r\n"
    "level = 1;\r\n"
    "localStorage.setItem('user_xp', 0);\r\n"
    "localStorage.setItem('user_level', 1);\r\n"
    "if (typeof updateGamificationHeader === 'function') updateGamificationHeader();"
).encode('utf-8')

if old_submit_xp_reset in content:
    content = content.replace(old_submit_xp_reset, new_submit_xp_reset, 1)
    print("SUCCESS 1: Added XP reset to 0 for fresh Day 1 onboarding start")
else:
    print("WARNING 1: Could not find old_submit_xp_reset")

with open('index.html', 'wb') as f:
    f.write(content)

print("File written.")
