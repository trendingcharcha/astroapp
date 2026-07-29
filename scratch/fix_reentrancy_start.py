with open('index.html', 'rb') as f:
    content = f.read()

target = b"function setAppLanguage(lang) {\r\n"
replacement = b"let _isSettingAppLang = false;\r\nfunction setAppLanguage(lang) {\r\nif (_isSettingAppLang) return;\r\n_isSettingAppLang = true;\r\ntry {\r\n"

if target in content:
    content = content.replace(target, replacement, 1)
    print("SUCCESS: Added re-entrancy guard to start of setAppLanguage")
else:
    print("WARNING: target not found")

with open('index.html', 'wb') as f:
    f.write(content)
