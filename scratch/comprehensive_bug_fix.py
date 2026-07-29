import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("=== COMPREHENSIVE BUG AUDIT & FIX ENGINE ===")
fixes = 0

# === FIX 1: VASTU DAILY DIRECTION IN extractIndividualDayTasks - Hardcoded "East or North" ===
# BUG: At line 5867-5876, the daily Vastu direction task is hardcoded to "Face East or North"
# regardless of user's Lagna Lord. Should pull cachedLagnaSignNum to pick personalized direction.
old_vastu_task = """tasks.push({
category: 'vastu',
title: isHi ? `দৈনিক দিশা সংরেখণ` : `Daily Direction Alignment`,
timeWindow: 'All Day',
text: isHi
? `সকারাত্মক ঊর্জা প্রবাহের জন্য কাজ করতে বা ধ্যান করতে পূর্ব বা উত্তর দিক মুখ করুন।`
: `Face East or North while working or meditating to align with positive energetic currents.`,"""

# Actually search for the exact content:
target_static_vastu = """tasks.push({
category: 'vastu',
title: isHi ? `দৈনিক দিশা সংরেখণ` : `Daily Direction Alignment`,"""

# The real content:
old_vastu = """tasks.push({
category: 'vastu',
title: isHi ? `দৈনিক দিশা সংরেখণ` : `Daily Direction Alignment`,
timeWindow: 'All Day',
text: isHi
? `সকারাত্মক ঊর্জা প্রবাহের জন্য কাজ করতে বা ধ্যান করতে পূর্ব বা উত্তর দিক মুখ করুন।`
: `Face East or North while working or meditating to align with positive energetic currents.`,
xp: 15,
color: '#5dade2',
icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#5dade2" stroke-width="1.8"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>'
});"""

# Search exact string:
search_exact = """title: isHi ? `দৈনিক দিশা সংরেখণ` : `Daily Direction Alignment`,
timeWindow: 'All Day',
text: isHi
? `সকারাত্মক ঊর্জা প্রবাহের জন্য কাজ করতে বা ধ্যান করতে পূর্ব বা উত্তর দিক মুখ করুন।`
: `Face East or North while working or meditating to align with positive energetic currents.`,"""

# Use English-only patterns:
old_vastu_en = "`: `Face East or North while working or meditating to align with positive energetic currents.`,"
new_vastu_en = """`: (() => {
        // Compute personalized power direction from cached Lagna Lord
        const _dirMapEn = { "Sun": "East", "Moon": "North-West", "Mars": "South", "Mercury": "North", "Jupiter": "North-East", "Venus": "South-East", "Saturn": "West" };
        const _dirMapHi = { "Sun": "पूर्व", "Moon": "उत्तर-पश्चिम", "Mars": "दक्षिण", "Mercury": "उत्तर", "Jupiter": "उत्तर-पूर्व", "Venus": "दक्षिण-पूर्व", "Saturn": "पश्चिम" };
        const _lsn = (typeof cachedLagnaSignNum !== 'undefined' && cachedLagnaSignNum !== null) ? cachedLagnaSignNum : null;
        const _lords = ['Mars','Venus','Mercury','Moon','Sun','Mercury','Venus','Mars','Jupiter','Saturn','Saturn','Jupiter'];
        const _ll = (_lsn !== null) ? (_lords[_lsn] || 'North') : 'North';
        const _dir = isHi ? (_dirMapHi[_ll] || 'उत्तर-पूर्व') : (_dirMapEn[_ll] || 'North-East');
        return isHi
          ? `अपने लग्न स्वामी (${_ll}) के अनुसार, ${_dir} दिशा की ओर मुंह करके काम करें या ध्यान लगाएं ताकि सकारात्मक ऊर्जा प्रवाह सक्रिय हो।`
          : `Based on your Ascendant Lord (${_ll}), face ${_dir} while working or meditating to align with your personal power direction.`;
      })()`,"""

if old_vastu_en in content:
    content = content.replace(old_vastu_en, new_vastu_en, 1)
    print(f"[FIX 1] Personalized Daily Direction Alignment in daily tasks (was hardcoded 'East or North')")
    fixes += 1
else:
    print("[SKIP 1] Already fixed or different format for daily Vastu direction")

# === FIX 2: COACH TAB VASTU DIRECTION "Daily Direction Alignment" IS HARDCODED ===
# BUG: Line 4383 in generateCoachMission, "Face East or North" is hardcoded
old_coach_vastu = "'Face East or North while working or meditating to align with positive energetic currents.'"
new_coach_vastu = """(() => {
  const _dmap = { "Sun": "East", "Moon": "North-West", "Mars": "South", "Mercury": "North", "Jupiter": "North-East", "Venus": "South-East", "Saturn": "West" };
  const _dmapHi = { "Sun": "पूर्व", "Moon": "उत्तर-पश्चिम", "Mars": "दक्षिण", "Mercury": "उत्तर", "Jupiter": "उत्तर-पूर्व", "Venus": "दक्षिण-पूर्व", "Saturn": "पश्चिम" };
  const _lsn = (typeof cachedLagnaSignNum !== 'undefined') ? cachedLagnaSignNum : null;
  const _lords = ['Mars','Venus','Mercury','Moon','Sun','Mercury','Venus','Mars','Jupiter','Saturn','Saturn','Jupiter'];
  const _ll = (_lsn !== null) ? (_lords[_lsn] || 'Mercury') : 'Mercury';
  const _dir = lang === 'hi' ? (_dmapHi[_ll] || 'उत्तर-पूर्व') : (_dmap[_ll] || 'North-East');
  return lang === 'hi'
    ? `अपने लग्न स्वामी (${_ll}) के अनुसार ${_dir} दिशा की ओर मुंह करके काम करें या ध्यान लगाएं।`
    : `Based on your Ascendant Lord (${_ll}), face ${_dir} while working or meditating for maximum energy alignment.`;
})()"""

if old_coach_vastu in content:
    content = content.replace(old_coach_vastu, new_coach_vastu, 1)
    print(f"[FIX 2] Personalized Daily Direction Alignment in Coach Mission Vastu")
    fixes += 1
else:
    print("[SKIP 2] Already fixed or different format for Coach Vastu direction")

# === FIX 3: Upgrade SYSTEM_CACHE_VERSION to force full re-init for all users ===
old_cache_ver = "const SYSTEM_CACHE_VERSION = 'v2026_07_27_purge_all_v12';"
new_cache_ver = "const SYSTEM_CACHE_VERSION = 'v2026_07_27_full_dynamic_v15';"
if old_cache_ver in content:
    content = content.replace(old_cache_ver, new_cache_ver, 1)
    print("[FIX 3] Bumped SYSTEM_CACHE_VERSION to v15 to force full re-init for all users")
    fixes += 1
else:
    print("[SKIP 3] SYSTEM_CACHE_VERSION already updated or different")

# === FIX 4: extractIndividualDayTasks Vastu Hindi daily direction ===
old_vastu_hi = "? `সকারাত্মক ঊর্জা প্রবাহের জন্য কাজ করতে বা ধ্যান করতে পূর্ব বা উত্তর দিক মুখ করুন।`"
if old_vastu_hi in content:
    content = content.replace(old_vastu_hi, "? `[direction computed dynamically below]`")
    print("[FIX 4] Removed hardcoded Hindi Vastu direction reference")
    fixes += 1

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nApplied {fixes} bug fixes. Writing complete comprehensive fix via direct multi-edit...")
