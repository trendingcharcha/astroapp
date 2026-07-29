with open('index.html', 'rb') as f:
    content = f.read()

old_cache_section = (
    "// GLOBAL CACHE PURGE ENGINE (Purges old stale cache for all existing & new users)\r\n"
    "  const SYSTEM_CACHE_VERSION = 'v2026_07_27_fresh_release_v100';"
).encode('utf-8')

new_cache_section = (
    "// ═══════════════════════════════════════════════════════════════\r\n"
    "// TIMELY AUTO-PURGE & REAL-TIME ALIGNMENT ENGINE\r\n"
    "// Automatically flushes stale daily caches on date shift, version bump,\r\n"
    "// or backend sync, ensuring 100% updated data on Web & Flutter WebView.\r\n"
    "// ═══════════════════════════════════════════════════════════════\r\n"
    "function checkTimelyAutoPurge() {\r\n"
    "  const todayStr = typeof getFormattedDate === 'function' ? getFormattedDate() : new Date().toISOString().split('T')[0];\r\n"
    "  const lastPurgeDate = localStorage.getItem('last_timely_purge_date');\r\n"
    "\r\n"
    "  if (lastPurgeDate !== todayStr) {\r\n"
    "    console.log('[Astro AI] Timely Auto-Purge executing for date:', todayStr);\r\n"
    "    const dailyKeysToPurge = [\r\n"
    "      'today_mission_date',\r\n"
    "      'today_quest_vedic_text', 'today_quest_lalkitab_text',\r\n"
    "      'today_quest_vastu_text', 'today_quest_practical_text',\r\n"
    "      'today_quest_vedic_text_en', 'today_quest_vedic_text_hi',\r\n"
    "      'today_quest_lalkitab_text_en', 'today_quest_lalkitab_text_hi',\r\n"
    "      'today_quest_vastu_text_en', 'today_quest_vastu_text_hi',\r\n"
    "      'today_quest_practical_text_en', 'today_quest_practical_text_hi',\r\n"
    "      'today_mission_vedic_en', 'today_mission_vedic_hi',\r\n"
    "      'today_mission_lalkitab_en', 'today_mission_lalkitab_hi',\r\n"
    "      'today_mission_vastu_en', 'today_mission_vastu_hi',\r\n"
    "      'today_mission_practical_en', 'today_mission_practical_hi',\r\n"
    "      'today_mission_title_en', 'today_mission_title_hi',\r\n"
    "      'today_astro_prediction_en', 'today_astro_prediction_hi',\r\n"
    "      'daily_sanatan_notif_en', 'daily_sanatan_notif_hi', 'daily_notif_date',\r\n"
    "      'karma_daily_vastu_dir', 'karma_daily_lagna_lord'\r\n"
    "    ];\r\n"
    "    dailyKeysToPurge.forEach(k => localStorage.removeItem(k));\r\n"
    "    localStorage.setItem('last_timely_purge_date', todayStr);\r\n"
    "\r\n"
    "    // Auto-generate fresh active daily mission & quests for TODAY\r\n"
    "    try {\r\n"
    "      if (typeof generateCoachMission === 'function') {\r\n"
    "        generateCoachMission({ preventDefault: () => {} });\r\n"
    "      }\r\n"
    "    } catch(e) {}\r\n"
    "\r\n"
    "    // Update Sanatan notifications for TODAY\r\n"
    "    try {\r\n"
    "      if (typeof updateSanatanNotifications === 'function') {\r\n"
    "        updateSanatanNotifications(currentAppLang);\r\n"
    "      }\r\n"
    "    } catch(e) {}\r\n"
    "\r\n"
    "    console.log('[Astro AI] Timely Auto-Purge Complete. System aligned to', todayStr);\r\n"
    "  }\r\n"
    "}\r\n"
    "\r\n"
    "// Start 60-second background alignment timer for midnight date shifts\r\n"
    "setInterval(checkTimelyAutoPurge, 60000);\r\n"
    "\r\n"
    "// GLOBAL CACHE PURGE ENGINE (Purges old stale cache for all existing & new users)\r\n"
    "  const SYSTEM_CACHE_VERSION = 'v2026_07_28_auto_purge_engine_v200';"
).encode('utf-8')

if old_cache_section in content:
    content = content.replace(old_cache_section, new_cache_section, 1)
    print("SUCCESS 1: Added Timely Auto-Purge Engine & bumped SYSTEM_CACHE_VERSION")
else:
    print("WARNING 1: Could not find old_cache_section")

old_initapp_call = "// --- INITIALIZE GAMIFICATION AND RESTORE MISSION ---".encode('utf-8')
new_initapp_call = "checkTimelyAutoPurge();\r\n\r\n// --- INITIALIZE GAMIFICATION AND RESTORE MISSION ---".encode('utf-8')

if old_initapp_call in content:
    content = content.replace(old_initapp_call, new_initapp_call, 1)
    print("SUCCESS 2: Added checkTimelyAutoPurge() call inside initApp()")
else:
    print("WARNING 2: Could not find old_initapp_call")

with open('index.html', 'wb') as f:
    f.write(content)

print("File written.")
