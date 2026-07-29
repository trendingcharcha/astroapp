with open('index.html', 'rb') as f:
    content = f.read()

checks = [
    ("1. generateChart does NOT call setAppLanguage", b"setKundliLang(kundliLang); setAppLanguage(" not in content),
    ("2. _isSettingAppLang reentrancy guard exists", b"_isSettingAppLang" in content),
    ("3. setAppLanguage checks cachedPlacementsList before report re-renders", b"if (typeof cachedPlacementsList !== 'undefined' && cachedPlacementsList && cachedPlacementsList.length > 0)" in content),
    ("4. loadCloudConfig has null check for db-url", b"if (urlEl) urlEl.value = url;" in content),
    ("5. dismissSplashScreen has try/catch fail-safe", b"try {\r\nconst isAuthFlag = localStorage.getItem('user_authenticated') === 'true';" in content),
]

all_pass = True
for title, test in checks:
    status = "PASS" if test else "FAIL"
    if not test: all_pass = False
    print(f"{status}: {title}")

print("\n" + ("ALL INFINITE LOOP & LOAD CHECKS PASSED!" if all_pass else "SOME CHECKS FAILED"))
