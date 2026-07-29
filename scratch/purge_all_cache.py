with open('index.html', 'rb') as f:
    content = f.read()

# 1. Bump APP_CACHE_VER at head
old_head_ver = b"var APP_CACHE_VER = 'cv_20260723_r3';"
new_head_ver = b"var APP_CACHE_VER = 'cv_20260727_r100_fresh';"

# 2. Bump SYSTEM_CACHE_VERSION at line 9363
old_sys_ver = b"const SYSTEM_CACHE_VERSION = 'v2026_07_27_full_dynamic_v15';"
new_sys_ver = b"const SYSTEM_CACHE_VERSION = 'v2026_07_27_fresh_release_v100';"

if old_head_ver in content:
    content = content.replace(old_head_ver, new_head_ver, 1)
    print("SUCCESS 1: Bumped head APP_CACHE_VER to cv_20260727_r100_fresh")
else:
    print("WARNING 1: Could not find old_head_ver")

if old_sys_ver in content:
    content = content.replace(old_sys_ver, new_sys_ver, 1)
    print("SUCCESS 2: Bumped SYSTEM_CACHE_VERSION to v2026_07_27_fresh_release_v100")
else:
    print("WARNING 2: Could not find old_sys_ver")

with open('index.html', 'wb') as f:
    f.write(content)

print("File written.")
