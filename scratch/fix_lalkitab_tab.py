with open('index.html', 'rb') as f:
    content = f.read()

# 1. Update switchTab function to activate tabs IMMEDIATELY at function start
old_switchTab = (
    b"async function switchTab(index, btn) {\r\n"
    b"// TAB 3: MATCHING - Auto-initialize Person 1 from stored profile\r\n"
    b"if (index === 3) {\r\n"
    b"if (typeof initMatchingForm === 'function') {\r\n"
    b"initMatchingForm();\r\n"
    b"}\r\n"
    b"}\r\n"
    b"// TAB 2: LAL KITAB - Generate report and draw fixed chart\r\n"
    b"if (index === 2) {\r\n"
    b"if (typeof generateLalKitabReport === 'function') {\r\n"
    b"// await to prevent double-generateChart race condition\r\n"
    b"await generateLalKitabReport();\r\n"
    b"}\r\n"
    b"}\r\n"
    b"// TAB 4: VASTU - Generate personalized Vastu report\r\n"
    b"if (index === 4) {\r\n"
    b"    if (typeof generatePersonalizedVastuReport === 'function') {\r\n"
    b"      generatePersonalizedVastuReport().then(() => {\r\n"
    b"        const notCalc = document.getElementById('vastu-not-calculated-view');\r\n"
    b"        const resView = document.getElementById('vastu-result-view');\r\n"
    b"        if (notCalc && resView) {\r\n"
    b"          notCalc.style.display = 'none';\r\n"
    b"          resView.style.display = 'block';\r\n"
    b"        }\r\n"
    b"      });\r\n"
    b"    }\r\n"
    b"  }\r\n"
    b"// Deactivate other tabs\r\n"
    b"document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));\r\n"
    b"document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));\r\n"
    b"// Activate target tab\r\n"
    b"const tabIds = ['tab-home', 'tab-kundli', 'tab-lalkitab', 'tab-matching', 'tab-vastu', 'tab-coach', 'tab-settings'];\r\n"
    b"const targetEl = document.getElementById(tabIds[index]);\r\n"
    b"if (targetEl) targetEl.classList.add('active');\r\n"
    b"if (btn) btn.classList.add('active');\r\n"
    b"\r\n"
    b"// TAB 1: KUNDLI - Automatically generate & show chart directly (Zero secondary form)\r\n"
    b"if (index === 1) {\r\n"
    b"const kForm = document.getElementById('kundli-form-view');\r\n"
    b"const kRes = document.getElementById('kundli-result-view');\r\n"
    b"if (kForm) kForm.style.display = 'none';\r\n"
    b"if (kRes) kRes.style.display = 'block';\r\n"
    b"// Await autoFill (which internally calls generateChart) before drawing \xe2\x80\x94 fixes race condition\r\n"
    b"await autoFillKundliFromOnboarding();\r\n"
    b"// drawChart is now safe to call since cachedPlacementsList is populated\r\n"
    b"if (typeof drawChart === 'function') drawChart();\r\n"
    b"}\r\n"
    b"\r\n"
    b"// TAB 5: COACH - Automatically generate & show active Mission for all goals\r\n"
    b"if (index === 5) {\r\n"
    b"const cForm = document.getElementById('coach-form-view');\r\n"
    b"const cRes = document.getElementById('coach-result-view');\r\n"
    b"if (cForm) cForm.style.display = 'none';\r\n"
    b"if (cRes) cRes.style.display = 'block';\r\n"
    b"if (typeof generateCoachMission === 'function') {\r\n"
    b"generateCoachMission();\r\n"
    b"}\r\n"
    b"}\r\n"
    b"}"
)

new_switchTab = (
    b"async function switchTab(index, btn) {\r\n"
    b"// 1. Instant tab & nav bar activation\r\n"
    b"document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));\r\n"
    b"document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));\r\n"
    b"const tabIds = ['tab-home', 'tab-kundli', 'tab-lalkitab', 'tab-matching', 'tab-vastu', 'tab-coach', 'tab-settings'];\r\n"
    b"const targetEl = document.getElementById(tabIds[index]);\r\n"
    b"if (targetEl) targetEl.classList.add('active');\r\n"
    b"const navItems = document.querySelectorAll('.nav-item');\r\n"
    b"if (navItems[index]) navItems[index].classList.add('active');\r\n"
    b"if (btn) btn.classList.add('active');\r\n"
    b"\r\n"
    b"// 2. Safe async tab data population\r\n"
    b"try {\r\n"
    b"if (index === 1) {\r\n"
    b"const kForm = document.getElementById('kundli-form-view');\r\n"
    b"const kRes = document.getElementById('kundli-result-view');\r\n"
    b"if (kForm) kForm.style.display = 'none';\r\n"
    b"if (kRes) kRes.style.display = 'block';\r\n"
    b"await autoFillKundliFromOnboarding();\r\n"
    b"if (typeof drawChart === 'function') drawChart();\r\n"
    b"} else if (index === 2) {\r\n"
    b"if (typeof generateLalKitabReport === 'function') {\r\n"
    b"await generateLalKitabReport();\r\n"
    b"}\r\n"
    b"} else if (index === 3) {\r\n"
    b"if (typeof initMatchingForm === 'function') {\r\n"
    b"initMatchingForm();\r\n"
    b"}\r\n"
    b"} else if (index === 4) {\r\n"
    b"if (typeof generatePersonalizedVastuReport === 'function') {\r\n"
    b"await generatePersonalizedVastuReport();\r\n"
    b"const notCalc = document.getElementById('vastu-not-calculated-view');\r\n"
    b"const resView = document.getElementById('vastu-result-view');\r\n"
    b"if (notCalc && resView) {\r\n"
    b"notCalc.style.display = 'none';\r\n"
    b"resView.style.display = 'block';\r\n"
    b"}\r\n"
    b"}\r\n"
    b"} else if (index === 5) {\r\n"
    b"const cForm = document.getElementById('coach-form-view');\r\n"
    b"const cRes = document.getElementById('coach-result-view');\r\n"
    b"if (cForm) cForm.style.display = 'none';\r\n"
    b"if (cRes) cRes.style.display = 'block';\r\n"
    b"if (typeof generateCoachMission === 'function') {\r\n"
    b"await generateCoachMission();\r\n"
    b"}\r\n"
    b"}\r\n"
    b"} catch(err) {\r\n"
    b"console.error('[Astro AI] switchTab error:', err);\r\n"
    b"}\r\n"
    b"}"
)

# 2. Fix generateLalKitabReport to properly await autoFillKundliFromOnboarding
old_lalkitab_autofill = (
    b"// 1. Auto-fill master details & calculate placements if not generated yet\r\n"
    b"if (!cachedPlacementsList || cachedPlacementsList.length === 0) {\r\n"
    b"autoFillKundliFromOnboarding();\r\n"
    b"if (typeof generateChart === 'function') {\r\n"
    b"await generateChart({ preventDefault: () => {} });\r\n"
    b"}\r\n"
    b"}"
)

new_lalkitab_autofill = (
    b"// 1. Auto-fill master details & calculate placements if not generated yet\r\n"
    b"if (!cachedPlacementsList || cachedPlacementsList.length === 0) {\r\n"
    b"if (typeof autoFillKundliFromOnboarding === 'function') {\r\n"
    b"await autoFillKundliFromOnboarding();\r\n"
    b"} else if (typeof generateChart === 'function') {\r\n"
    b"await generateChart({ preventDefault: () => {} });\r\n"
    b"}\r\n"
    b"}"
)

# 3. Fix generatePersonalizedVastuReport to properly await autoFillKundliFromOnboarding
old_vastu_autofill = (
    b"// If placements not loaded, auto-fill and calculate chart\r\n"
    b"if (!cachedPlacementsList || cachedPlacementsList.length === 0) {\r\n"
    b"autoFillKundliFromOnboarding();\r\n"
    b"if (typeof generateChart === 'function') {\r\n"
    b"await generateChart({ preventDefault: () => {} });\r\n"
    b"}\r\n"
    b"}"
)

new_vastu_autofill = (
    b"// If placements not loaded, auto-fill and calculate chart\r\n"
    b"if (!cachedPlacementsList || cachedPlacementsList.length === 0) {\r\n"
    b"if (typeof autoFillKundliFromOnboarding === 'function') {\r\n"
    b"await autoFillKundliFromOnboarding();\r\n"
    b"} else if (typeof generateChart === 'function') {\r\n"
    b"await generateChart({ preventDefault: () => {} });\r\n"
    b"}\r\n"
    b"}"
)

# Check and apply
if old_switchTab in content:
    content = content.replace(old_switchTab, new_switchTab, 1)
    print("SUCCESS: Updated switchTab for instant visual tab switching")
else:
    print("WARNING: Could not find exact old_switchTab")

if old_lalkitab_autofill in content:
    content = content.replace(old_lalkitab_autofill, new_lalkitab_autofill, 1)
    print("SUCCESS: Updated generateLalKitabReport with await autoFillKundliFromOnboarding")
else:
    print("WARNING: Could not find exact old_lalkitab_autofill")

if old_vastu_autofill in content:
    content = content.replace(old_vastu_autofill, new_vastu_autofill, 1)
    print("SUCCESS: Updated generatePersonalizedVastuReport with await autoFillKundliFromOnboarding")
else:
    print("WARNING: Could not find exact old_vastu_autofill")

with open('index.html', 'wb') as f:
    f.write(content)

print("File written.")
