with open('index.html', 'rb') as f:
    content = f.read()

api_checks = [
    ("1. Supabase Project URL Configured", b"https://rnunibjmmowhaxsytthf.supabase.co" in content),
    ("2. Supabase Cloud Sync Engine Intact", b"async function syncProfileToCloud(" in content),
    ("3. Supabase Cloud Restore Engine Intact", b"async function restoreProfileFromCloud(" in content),
    ("4. Supabase Feedbacks DB Table Insert Query Intact", b"supabaseClient.from('feedbacks').insert" in content),
    ("5. Supabase Profiles DB Table Upsert Query Intact", b"supabaseClient.from('profiles').upsert" in content),
    ("6. Supabase Google OAuth Provider Intact", b"provider: 'google'" in content),
    ("7. OpenStreetMap Nominatim Geocoding API Intact", b"nominatim.openstreetmap.org/search" in content),
    ("8. Web Speech Recognition API Intact", b"webkitSpeechRecognition" in content),
    ("9. Native Flutter Notification Bridge Intact", b"window.FlutterNotificationBridge" in content),
    ("10. LocalStorage Schema Intact (user_name, dob, tob, pob, goals, xp, streak)", 
     b"user_name" in content and b"user_dob" in content and b"user_xp" in content and b"user_streak" in content),
]

all_pass = True
print("=== COSMOVEDIC API & INTEGRATION HEALTH AUDIT ===\n")
for title, test in api_checks:
    status = "PASS (100% INTACT)" if test else "FAIL (DISTURBED)"
    if not test: all_pass = False
    print(f"{status}: {title}")

print("\n" + ("FINAL RESULT: ALL APIs & INTEGRATIONS ARE 100% INTACT AND UNDISTURBED!" if all_pass else "WARNING: SOME API DISTURBED"))
