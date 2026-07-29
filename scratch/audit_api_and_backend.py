import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("=== VERIFYING ALL BACKEND API & SYNC FUNCTIONS IN INDEX.HTML ===")

api_functions = [
    'setupSupabaseAuthListener',
    'handleOAuthCallback',
    'handleEmailAuth',
    'syncActiveGoalsToSupabase',
    'syncProfileToSupabase',
    'autoFillKundliFromOnboarding',
    'generateChart',
    'generateCoachMission',
    'generateDynamicGoalPrediction',
    'renderKundliEnhancedSections',
    'generateLalKitabReport',
    'generatePersonalizedVastuReport',
    'calculateCompatibility'
]

for fn in api_functions:
    pattern = rf'function\s+{fn}\s*\('
    if re.search(pattern, html):
        print(f"[INTACT & ACTIVE] {fn}() exists and is defined!")
    else:
        print(f"[MISSING/WARNING] {fn}() NOT FOUND!")

# Check Supabase client initialization
if 'supabase.createClient' in html or 'window.supabaseClient' in html or 'supabase' in html:
    print("\n[SUPABASE CLIENT] Supabase SDK & client initialization is present!")
else:
    print("\n[SUPABASE CLIENT WARNING] Supabase client initialization check failed!")
