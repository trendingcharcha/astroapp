import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("=== APPLYING GLOBAL CACHE PURGE ENGINE IN INDEX.HTML ===")

target = """// 1-TIME CACHE MIGRATION ENGINE (Purges old stale dummy task cache for existing users)
const SYSTEM_CACHE_VERSION = 'v2026_07_26_custom_engine_v5';
const userCacheVer = localStorage.getItem('app_cache_version');

if (userCacheVer !== SYSTEM_CACHE_VERSION) {
const keysToPurge = [
'today_mission_date', 'today_quest_vedic_text', 'today_quest_lalkitab_text',
'today_quest_vastu_text', 'today_quest_practical_text',
'today_mission_vedic_en', 'today_mission_vedic_hi',
'today_mission_lalkitab_en', 'today_mission_lalkitab_hi',
'today_mission_vastu_en', 'today_mission_vastu_hi',
'today_mission_practical_en', 'today_mission_practical_hi',
'today_mission_title_en', 'today_mission_title_hi',
'today_astro_prediction_en', 'today_astro_prediction_hi'
];
keysToPurge.forEach(k => localStorage.removeItem(k));
localStorage.setItem('app_cache_version', SYSTEM_CACHE_VERSION);
}"""

replacement = """// GLOBAL CACHE PURGE ENGINE (Purges old stale cache for all existing & new users)
  const SYSTEM_CACHE_VERSION = 'v2026_07_27_purge_all_v12';
  const userCacheVer = localStorage.getItem('app_cache_version');

  if (userCacheVer !== SYSTEM_CACHE_VERSION) {
    const keysToPurge = [
      'today_mission_date', 'today_quest_vedic_text', 'today_quest_lalkitab_text',
      'today_quest_vastu_text', 'today_quest_practical_text',
      'today_mission_vedic_en', 'today_mission_vedic_hi',
      'today_mission_lalkitab_en', 'today_mission_lalkitab_hi',
      'today_mission_vastu_en', 'today_mission_vastu_hi',
      'today_mission_practical_en', 'today_mission_practical_hi',
      'today_mission_title_en', 'today_mission_title_hi',
      'today_astro_prediction_en', 'today_astro_prediction_hi',
      'cachedPlacementsList', 'cachedLagnaSignNum', 'cachedBirthDateStr'
    ];
    keysToPurge.forEach(k => localStorage.removeItem(k));

    // Clear browser CacheStorage for PWA / ServiceWorker if active
    if ('caches' in window) {
      caches.keys().then(names => {
        names.forEach(name => caches.delete(name));
      }).catch(e => {});
    }

    localStorage.setItem('app_cache_version', SYSTEM_CACHE_VERSION);
  }"""

if target in content:
    content = content.replace(target, replacement, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESSFULLY UPDATED GLOBAL CACHE PURGE ENGINE IN INDEX.HTML!")
else:
    print("ERROR: Target cache version block not found in index.html")
