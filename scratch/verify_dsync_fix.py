with open('index.html', 'rb') as f:
    content = f.read()

checks = [
    ("1. APP_CACHE_VER is cv_20260728_v500_release", b"var APP_CACHE_VER = 'cv_20260728_v500_release';" in content),
    ("2. Head URL check matches exact version _cb=APP_CACHE_VER", b"if (window.location.href.indexOf('_cb=' + APP_CACHE_VER) === -1)" in content),
    ("3. SYSTEM_CACHE_VERSION is v2026_07_28_v500_release", b"const SYSTEM_CACHE_VERSION = 'v2026_07_28_v500_release';" in content),
    ("4. restoreProfileFromCloud purges stale daily caches", b"if (cachedMissionDate !== todayStr)" in content),
]

all_pass = True
for title, test in checks:
    status = "PASS" if test else "FAIL"
    if not test: all_pass = False
    print(f"{status}: {title}")

print("\n" + ("ALL PHONE VS PC DESYNC CHECKS PASSED!" if all_pass else "SOME CHECKS FAILED"))
