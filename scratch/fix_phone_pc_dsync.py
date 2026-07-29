with open('index.html', 'rb') as f:
    content = f.read()

# 1. Update APP_CACHE_VER in head
old_head_ver = b"var APP_CACHE_VER = 'cv_20260727_r100_fresh';"
new_head_ver = b"var APP_CACHE_VER = 'cv_20260728_v500_release';"

# 2. Fix Step 5 URL check in head from indexOf('_cb=') to indexOf('_cb=' + APP_CACHE_VER)
old_url_check = b"if (window.location.href.indexOf('_cb=') === -1) {"
new_url_check = b"if (window.location.href.indexOf('_cb=' + APP_CACHE_VER) === -1) {"

# 3. Bump SYSTEM_CACHE_VERSION
old_sys_ver = b"const SYSTEM_CACHE_VERSION = 'v2026_07_28_auto_purge_engine_v200';"
new_sys_ver = b"const SYSTEM_CACHE_VERSION = 'v2026_07_28_v500_release';"

# 4. Update restoreProfileFromCloud to purge stale daily caches and re-evaluate Coach Mission for TODAY
old_restore_end = (
    "localStorage.setItem('user_goal', goal);\r\n"
    "localStorage.setItem('onboarding_path', onboardingPath);\r\n"
    "return true;"
).encode('utf-8')

new_restore_end = (
    "localStorage.setItem('user_goal', goal);\r\n"
    "localStorage.setItem('onboarding_path', onboardingPath);\r\n"
    "\r\n"
    "// AUTO-PURGE & ALIGN TODAY'S MISSION FOR CLOUD RESTORED USERS\r\n"
    "const todayStr = typeof getFormattedDate === 'function' ? getFormattedDate() : new Date().toISOString().split('T')[0];\r\n"
    "const cachedMissionDate = localStorage.getItem('today_mission_date');\r\n"
    "if (cachedMissionDate !== todayStr) {\r\n"
    "  const keysToPurge = [\r\n"
    "    'today_mission_date', 'today_quest_vedic_text', 'today_quest_lalkitab_text',\r\n"
    "    'today_quest_vastu_text', 'today_quest_practical_text',\r\n"
    "    'today_mission_vedic_en', 'today_mission_vedic_hi',\r\n"
    "    'today_mission_lalkitab_en', 'today_mission_lalkitab_hi',\r\n"
    "    'today_mission_vastu_en', 'today_mission_vastu_hi',\r\n"
    "    'today_mission_practical_en', 'today_mission_practical_hi',\r\n"
    "    'today_mission_title_en', 'today_mission_title_hi',\r\n"
    "    'today_astro_prediction_en', 'today_astro_prediction_hi',\r\n"
    "    'daily_sanatan_notif_en', 'daily_sanatan_notif_hi', 'daily_notif_date'\r\n"
    "  ];\r\n"
    "  keysToPurge.forEach(k => localStorage.removeItem(k));\r\n"
    "  try {\r\n"
    "    if (typeof generateCoachMission === 'function') {\r\n"
    "      generateCoachMission({ preventDefault: () => {} });\r\n"
    "    }\r\n"
    "  } catch(e) {}\r\n"
    "}\r\n"
    "return true;"
).encode('utf-8')

# Apply replacements
if old_head_ver in content:
    content = content.replace(old_head_ver, new_head_ver, 1)
    print("SUCCESS 1: Bumped head APP_CACHE_VER to cv_20260728_v500_release")
else:
    print("WARNING 1: Could not find old_head_ver")

if old_url_check in content:
    content = content.replace(old_url_check, new_url_check, 1)
    print("SUCCESS 2: Fixed head URL check to match exact version _cb=APP_CACHE_VER")
else:
    print("WARNING 2: Could not find old_url_check")

if old_sys_ver in content:
    content = content.replace(old_sys_ver, new_sys_ver, 1)
    print("SUCCESS 3: Bumped SYSTEM_CACHE_VERSION to v2026_07_28_v500_release")
else:
    print("WARNING 3: Could not find old_sys_ver")

if old_restore_end in content:
    content = content.replace(old_restore_end, new_restore_end, 1)
    print("SUCCESS 4: Updated restoreProfileFromCloud to purge stale daily caches")
else:
    print("WARNING 4: Could not find old_restore_end")

with open('index.html', 'wb') as f:
    f.write(content)

print("File written.")
