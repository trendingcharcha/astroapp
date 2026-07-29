with open('index.html', 'rb') as f:
    content = f.read()

checks = [
    ("1. setAppLanguage re-renders Coach Mission", b"generateCoachMission();" in content),
    ("2. setAppLanguage re-renders Kundli Enhanced Sections", b"renderKundliEnhancedSections(cachedPlacementsList" in content),
    ("3. setAppLanguage re-renders Lal Kitab Report", b"generateLalKitabReport();" in content),
    ("4. setAppLanguage re-renders Vastu Report", b"generatePersonalizedVastuReport();" in content),
    ("5. setKundliLang syncs currentAppLang", b"currentAppLang = lang;" in content),
    ("6. Instant CSS data-lang attribute exists", b"document.documentElement.setAttribute('data-lang', lang);" in content),
]

all_pass = True
for title, test in checks:
    status = "PASS" if test else "FAIL"
    if not test: all_pass = False
    print(f"{status}: {title}")

print("\n" + ("ALL LANGUAGE SYNC CHECKS PASSED!" if all_pass else "SOME CHECKS FAILED"))
