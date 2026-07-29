with open('index.html', 'rb') as f:
    content = f.read()

# 1. Update APP_CACHE_VER to force browser hard refresh
content = content.replace(
    b"var APP_CACHE_VER = 'cv_20260728_TOTAL_GLOBAL_PURGE_v999';",
    b"var APP_CACHE_VER = 'cv_20260728_TOTAL_GLOBAL_PURGE_v1002';"
)

target = (
    b".btn:hover {\r\n"
    b"transform: translateY(-2px);\r\n"
    b"box-shadow: var(--btn-shadow);\r\n"
    b"filter: brightness(1.05);\r\n"
    b"}"
)

replacement = (
    b".btn:hover {\r\n"
    b"transform: translateY(-2px);\r\n"
    b"box-shadow: var(--btn-shadow);\r\n"
    b"filter: brightness(1.05);\r\n"
    b"}\r\n\r\n"
    b"/* STRICT LEFT ALIGNMENT FOR WIZARD & MODAL BUTTONS */\r\n"
    b"#livechat-messages .btn, #livechat-messages .btn-outline, #livechat-messages button, .btn-left {\r\n"
    b"  justify-content: flex-start !important;\r\n"
    b"  text-align: left !important;\r\n"
    b"  padding-left: 18px !important;\r\n"
    b"  display: flex !important;\r\n"
    b"  align-items: center !important;\r\n"
    b"  width: 100% !important;\r\n"
    b"}"
)

if target in content:
    content = content.replace(target, replacement, 1)
    print("SUCCESS: Added strict button left-alignment CSS rules and cache version v1002")
else:
    print("WARNING: target not found")

with open('index.html', 'wb') as f:
    f.write(content)

print("File written.")
