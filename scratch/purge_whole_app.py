with open('index.html', 'rb') as f:
    content = f.read()

# 1. Update APP_CACHE_VER in head
old_head_ver = b"var APP_CACHE_VER = 'cv_20260728_v500_release';"
new_head_ver = b"var APP_CACHE_VER = 'cv_20260728_TOTAL_GLOBAL_PURGE_v999';"

# 2. Update SYSTEM_CACHE_VERSION
old_sys_ver = b"const SYSTEM_CACHE_VERSION = 'v2026_07_28_v500_release';"
new_sys_ver = b"const SYSTEM_CACHE_VERSION = 'v2026_07_28_TOTAL_GLOBAL_PURGE_v999';"

if old_head_ver in content:
    content = content.replace(old_head_ver, new_head_ver, 1)
    print("SUCCESS 1: Bumped head APP_CACHE_VER to cv_20260728_TOTAL_GLOBAL_PURGE_v999")
else:
    print("WARNING 1: Could not find old_head_ver")

if old_sys_ver in content:
    content = content.replace(old_sys_ver, new_sys_ver, 1)
    print("SUCCESS 2: Bumped SYSTEM_CACHE_VERSION to v2026_07_28_TOTAL_GLOBAL_PURGE_v999")
else:
    print("WARNING 2: Could not find old_sys_ver")

with open('index.html', 'wb') as f:
    f.write(content)

print("File written.")
