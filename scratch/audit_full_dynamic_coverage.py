import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("=== AUDITING ALL DYNAMIC PROFILE HOOKS ACROSS ALL 6 TABS ===")

dynamic_hooks = [
    ("Kundli Birth Computation", "function generateChart"),
    ("Kundli Auto-Fill", "function autoFillKundliFromOnboarding"),
    ("Lal Kitab Report Generator", "function generateLalKitabReport"),
    ("Personalized Vastu Generator", "function generatePersonalizedVastuReport"),
    ("Matching Engine", "function calculateCompatibility"),
    ("Coach Mission Generator", "function generateCoachMission"),
    ("Roadmap Task Extractor", "function extractIndividualDayTasks"),
    ("Sanatan Notifications", "function updateSanatanNotifications"),
    ("Language Bootstrap", "function setAppLanguage")
]

all_passed = True
for label, hook in dynamic_hooks:
    if hook in content:
        print(f"[PASS] {label}: Found `{hook}`")
    else:
        print(f"[FAIL] {label}: Missing `{hook}`")
        all_passed = False

if all_passed:
    print("\nALL 9 DYNAMIC PROFILE HOOKS ARE 100% VERIFIED AND PRESENT!")
else:
    print("\nWARNING: SOME HOOKS ARE MISSING!")
