with open('index.html', 'rb') as f:
    content = f.read()

content = content.replace(
    b"var APP_CACHE_VER = 'cv_20260728_TOTAL_GLOBAL_PURGE_v1005';",
    b"var APP_CACHE_VER = 'cv_20260728_TOTAL_GLOBAL_PURGE_v1008';"
)

with open('index.html', 'wb') as f:
    f.write(content)

print("Bumped cache version to v1008")
