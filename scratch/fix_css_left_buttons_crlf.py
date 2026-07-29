with open('index.html', 'rb') as f:
    content = f.read()

target = (
    b"/* GLOBAL STRICT LEFT-ALIGNMENT RULE */\r\n"
    b".auth-card, .card, .modal, [id$=\"-modal\"], .form-group, #livechat-messages, #livechat-messages div, #onboarding-screen, #auth-screen {\r\n"
    b"  text-align: left !important;\r\n"
    b"}"
)

replacement = (
    b"/* GLOBAL STRICT LEFT-ALIGNMENT RULE */\r\n"
    b".auth-card, .card, .modal, [id$=\"-modal\"], .form-group, #livechat-messages, #livechat-messages div, #onboarding-screen, #auth-screen {\r\n"
    b"  text-align: left !important;\r\n"
    b"}\r\n\r\n"
    b"#livechat-messages button, #livechat-messages .btn, #livechat-messages .btn-outline {\r\n"
    b"  text-align: left !important;\r\n"
    b"  justify-content: flex-start !important;\r\n"
    b"  display: flex !important;\r\n"
    b"  align-items: center !important;\r\n"
    b"  width: 100% !important;\r\n"
    b"  box-sizing: border-box !important;\r\n"
    b"}"
)

if target in content:
    content = content.replace(target, replacement, 1)
    print("SUCCESS: Added strict button left-alignment CSS rules")
else:
    print("WARNING: target not found")

with open('index.html', 'wb') as f:
    f.write(content)

print("File written.")
