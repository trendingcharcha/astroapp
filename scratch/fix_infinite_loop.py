with open('index.html', 'rb') as f:
    content = f.read()

# 1. Remove setAppLanguage(currentAppLang) from inside generateChart() (line 10758)
old_genchart_lang = b"setKundliLang(kundliLang); setAppLanguage(currentAppLang);"
new_genchart_lang = b"setKundliLang(kundliLang);"

# 2. Wrap setAppLanguage with re-entrancy guard _isSettingAppLang
old_setAppLang = (
    b"function setAppLanguage(lang) {\r\n"
    b"currentAppLang = lang;\r\n"
    b"localStorage.setItem('app_language', lang);\r\n"
    b"\r\n"
    b"// \xe2\x80\x94\xe2\x80\x94 INSTANT CSS TOGGLE: sets one attribute \xe2\x86\x92 entire app switches \xe2\x80\x94\xe2\x80\x94\r\n"
    b"document.documentElement.setAttribute('data-lang', lang);"
)

new_setAppLang = (
    b"let _isSettingAppLang = false;\r\n"
    b"function setAppLanguage(lang) {\r\n"
    b"if (_isSettingAppLang) return;\r\n"
    b"_isSettingAppLang = true;\r\n"
    b"try {\r\n"
    b"currentAppLang = lang;\r\n"
    b"localStorage.setItem('app_language', lang);\r\n"
    b"\r\n"
    b"// \xe2\x80\x94\xe2\x80\x94 INSTANT CSS TOGGLE: sets one attribute \xe2\x86\x92 entire app switches \xe2\x80\x94\xe2\x80\x94\r\n"
    b"document.documentElement.setAttribute('data-lang', lang);"
)

# 3. Add finally block to end of setAppLanguage
old_setAppLang_end = (
    b"console.log('App language switched immediately to:', lang.toUpperCase());\r\n"
    b"}"
)

new_setAppLang_end = (
    b"console.log('App language switched immediately to:', lang.toUpperCase());\r\n"
    b"} finally {\r\n"
    b"_isSettingAppLang = false;\r\n"
    b"}\r\n"
    b"}"
)

# 4. Make setAppLanguage re-render reports ONLY when cachedPlacementsList ALREADY exists (no autoFill triggering)
old_report_rerenders = (
    b"// 9. Re-render Coach Cosmic Mission in target language\r\n"
    b"if (typeof generateCoachMission === 'function') {\r\n"
    b"generateCoachMission();\r\n"
    b"}\r\n"
    b"\r\n"
    b"// 10. Re-render Kundli Analysis Sections & Chart in target language\r\n"
    b"if (typeof cachedPlacementsList !== 'undefined' && cachedPlacementsList && cachedPlacementsList.length > 0) {\r\n"
    b"if (typeof renderKundliEnhancedSections === 'function') {\r\n"
    b"renderKundliEnhancedSections(cachedPlacementsList, cachedLagnaSignNum, cachedBirthDateStr || '');\r\n"
    b"}\r\n"
    b"if (typeof drawChart === 'function') {\r\n"
    b"drawChart();\r\n"
    b"}\r\n"
    b"}\r\n"
    b"\r\n"
    b"// 11. Re-render Lal Kitab Report in target language\r\n"
    b"if (typeof generateLalKitabReport === 'function') {\r\n"
    b"generateLalKitabReport();\r\n"
    b"}\r\n"
    b"\r\n"
    b"// 12. Re-render Personalized Vastu Report in target language\r\n"
    b"if (typeof generatePersonalizedVastuReport === 'function') {\r\n"
    b"generatePersonalizedVastuReport();\r\n"
    b"}"
)

new_report_rerenders = (
    b"// 9. Re-render reports ONLY if placements are already calculated (prevents circular autoFill calls)\r\n"
    b"if (typeof cachedPlacementsList !== 'undefined' && cachedPlacementsList && cachedPlacementsList.length > 0) {\r\n"
    b"if (typeof renderKundliEnhancedSections === 'function') {\r\n"
    b"renderKundliEnhancedSections(cachedPlacementsList, cachedLagnaSignNum, cachedBirthDateStr || '');\r\n"
    b"}\r\n"
    b"if (typeof drawChart === 'function') {\r\n"
    b"drawChart();\r\n"
    b"}\r\n"
    b"if (typeof generateLalKitabReport === 'function') {\r\n"
    b"generateLalKitabReport();\r\n"
    b"}\r\n"
    b"if (typeof generatePersonalizedVastuReport === 'function') {\r\n"
    b"generatePersonalizedVastuReport();\r\n"
    b"}\r\n"
    b"}\r\n"
    b"if (typeof generateCoachMission === 'function') {\r\n"
    b"generateCoachMission();\r\n"
    b"}"
)

# Apply fixes
if old_genchart_lang in content:
    content = content.replace(old_genchart_lang, new_genchart_lang, 1)
    print("SUCCESS 1: Removed circular setAppLanguage call from generateChart")
else:
    print("WARNING 1: Could not find old_genchart_lang")

if old_setAppLang in content:
    content = content.replace(old_setAppLang, new_setAppLang, 1)
    print("SUCCESS 2: Added re-entrancy guard start to setAppLanguage")
else:
    print("WARNING 2: Could not find old_setAppLang")

if old_report_rerenders in content:
    content = content.replace(old_report_rerenders, new_report_rerenders, 1)
    print("SUCCESS 3: Updated report re-renders to check cachedPlacementsList first")
else:
    print("WARNING 3: Could not find old_report_rerenders")

if old_setAppLang_end in content:
    content = content.replace(old_setAppLang_end, new_setAppLang_end, 1)
    print("SUCCESS 4: Added re-entrancy guard finally block to setAppLanguage")
else:
    print("WARNING 4: Could not find old_setAppLang_end")

with open('index.html', 'wb') as f:
    f.write(content)

print("File written.")
