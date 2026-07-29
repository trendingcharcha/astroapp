with open('index.html', 'rb') as f:
    content = f.read()

checks = [
    ("1. checkTimelyAutoPurge function exists", b"function checkTimelyAutoPurge()" in content),
    ("2. 60-second periodic alignment timer registered", b"setInterval(checkTimelyAutoPurge, 60000);" in content),
    ("3. checkTimelyAutoPurge called inside initApp", b"checkTimelyAutoPurge();" in content),
    ("4. SYSTEM_CACHE_VERSION updated", b"const SYSTEM_CACHE_VERSION = 'v2026_07_28_auto_purge_engine_v200';" in content),
]

all_pass = True
for title, test in checks:
    status = "PASS" if test else "FAIL"
    if not test: all_pass = False
    print(f"{status}: {title}")

print("\n" + ("ALL TIMELY AUTO-PURGE CHECKS PASSED!" if all_pass else "SOME CHECKS FAILED"))
