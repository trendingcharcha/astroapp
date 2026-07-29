with open('index.html', 'rb') as f:
    content = f.read().decode('utf-8')

# 1. Update APP_CACHE_VER to force browser hard refresh
content = content.replace(
    "var APP_CACHE_VER = 'cv_20260728_TOTAL_GLOBAL_PURGE_v999';",
    "var APP_CACHE_VER = 'cv_20260728_TOTAL_GLOBAL_PURGE_v1002';"
)

# 2. Add explicit CSS rule targeting ALL buttons inside livechat and modals
old_btn_rule = (
    ".btn:hover {\n"
    "transform: translateY(-2px);\n"
    "box-shadow: var(--btn-shadow);\n"
    "filter: brightness(1.05);\n"
    "}"
)

new_btn_rule = (
    ".btn:hover {\n"
    "transform: translateY(-2px);\n"
    "box-shadow: var(--btn-shadow);\n"
    "filter: brightness(1.05);\n"
    "}\n\n"
    "/* STRICT LEFT ALIGNMENT FOR WIZARD & MODAL BUTTONS */\n"
    "#livechat-messages .btn, #livechat-messages .btn-outline, #livechat-messages button, .btn-left {\n"
    "  justify-content: flex-start !important;\n"
    "  text-align: left !important;\n"
    "  padding-left: 18px !important;\n"
    "  display: flex !important;\n"
    "  align-items: center !important;\n"
    "  width: 100% !important;\n"
    "}"
)

if old_btn_rule in content:
    content = content.replace(old_btn_rule, new_btn_rule, 1)
    print("SUCCESS 1: Added explicit .btn-left left-alignment CSS rules")
else:
    print("WARNING 1: Could not find old_btn_rule")

with open('index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print("File written.")
