with open('index.html', 'rb') as f:
    content = f.read()

target = (
    b".auth-card {\r\n"
    b"background: var(--card-bg);\r\n"
    b"border: 1px solid var(--card-border);\r\n"
    b"backdrop-filter: blur(16px);\r\n"
    b"-webkit-backdrop-filter: blur(16px);\r\n"
    b"border-radius: 24px;\r\n"
    b"padding: 36px 26px;\r\n"
    b"width: 100%;\r\n"
    b"max-width: 420px;\r\n"
    b"box-shadow: 0 16px 40px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.08);\r\n"
    b"text-align: center;\r\n"
    b"margin-bottom: 30px;\r\n"
    b"}"
)

replacement = (
    b".auth-card {\r\n"
    b"background: var(--card-bg);\r\n"
    b"border: 1px solid var(--card-border);\r\n"
    b"backdrop-filter: blur(16px);\r\n"
    b"-webkit-backdrop-filter: blur(16px);\r\n"
    b"border-radius: 24px;\r\n"
    b"padding: 36px 26px;\r\n"
    b"width: 100%;\r\n"
    b"max-width: 420px;\r\n"
    b"box-shadow: 0 16px 40px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.08);\r\n"
    b"text-align: left !important;\r\n"
    b"margin-bottom: 30px;\r\n"
    b"}\r\n\r\n"
    b"/* GLOBAL STRICT LEFT-ALIGNMENT RULE */\r\n"
    b".auth-card, .card, .modal, [id$=\"-modal\"], .form-group, #livechat-messages, #livechat-messages div, #onboarding-screen, #auth-screen {\r\n"
    b"  text-align: left !important;\r\n"
    b"}"
)

if target in content:
    content = content.replace(target, replacement, 1)
    print("SUCCESS: Replaced .auth-card text-align center with text-align: left !important;")
else:
    print("WARNING: target not found")

with open('index.html', 'wb') as f:
    f.write(content)

print("File written.")
