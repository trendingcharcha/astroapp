with open('index.html', 'rb') as f:
    content = f.read()

# 1. Update setAppLanguage to re-render Coach Mission, Kundli Enhanced Sections, Lal Kitab & Vastu reports
old_setAppLang = (
    b"// 8. Re-render Karmic Journey grid with correct language\r\n"
    b"if (typeof renderKarmicJourney === 'function') {\r\n"
    b"renderKarmicJourney();\r\n"
    b"}\r\n"
    b"\r\n"
    b"console.log('<svg width=\"16\" height=\"16\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" style=\"vertical-align:middle; margin-right:4px;\"><circle cx=\"12\" cy=\"12\" r=\"10\"/><line x1=\"2\" y1=\"12\" x2=\"22\" y2=\"12\"/><path d=\"M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z\"/></svg> App language switched to:', lang.toUpperCase());\r\n"
    b"}"
)

new_setAppLang = (
    b"// 8. Re-render Karmic Journey grid with correct language\r\n"
    b"if (typeof renderKarmicJourney === 'function') {\r\n"
    b"renderKarmicJourney();\r\n"
    b"}\r\n"
    b"\r\n"
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
    b"}\r\n"
    b"\r\n"
    b"console.log('App language switched immediately to:', lang.toUpperCase());\r\n"
    b"}"
)

# 2. Update setKundliLang to also sync currentAppLang & data-lang
old_setKundliLang = (
    b"function setKundliLang(lang) {\r\n"
    b"kundliLang = lang;"
)

new_setKundliLang = (
    b"function setKundliLang(lang) {\r\n"
    b"kundliLang = lang;\r\n"
    b"if (typeof currentAppLang !== 'undefined' && currentAppLang !== lang) {\r\n"
    b"currentAppLang = lang;\r\n"
    b"localStorage.setItem('app_language', lang);\r\n"
    b"document.documentElement.setAttribute('data-lang', lang);\r\n"
    b"}"
)

if old_setAppLang in content:
    content = content.replace(old_setAppLang, new_setAppLang, 1)
    print("SUCCESS: Updated setAppLanguage to re-render all report screens instantly")
else:
    print("WARNING: Could not find old_setAppLang")

if old_setKundliLang in content:
    content = content.replace(old_setKundliLang, new_setKundliLang, 1)
    print("SUCCESS: Updated setKundliLang to sync global app language")
else:
    print("WARNING: Could not find old_setKundliLang")

with open('index.html', 'wb') as f:
    f.write(content)

print("File written.")
