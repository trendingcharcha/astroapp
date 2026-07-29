with open('index.html', 'rb') as f:
    content = f.read().decode('utf-8')

# 1. Update .auth-card class rule to text-align: left !important;
old_auth_card_css = (
    ".auth-card {\n"
    "background: var(--card-bg);\n"
    "border: 1px solid var(--card-border);\n"
    "backdrop-filter: blur(16px);\n"
    "-webkit-backdrop-filter: blur(16px);\n"
    "border-radius: 24px;\n"
    "padding: 36px 26px;\n"
    "width: 100%;\n"
    "max-width: 420px;\n"
    "box-shadow: 0 16px 40px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.08);\n"
    "text-align: center;\n"
    "margin-bottom: 30px;\n"
    "}"
)

new_auth_card_css = (
    ".auth-card {\n"
    "background: var(--card-bg);\n"
    "border: 1px solid var(--card-border);\n"
    "backdrop-filter: blur(16px);\n"
    "-webkit-backdrop-filter: blur(16px);\n"
    "border-radius: 24px;\n"
    "padding: 36px 26px;\n"
    "width: 100%;\n"
    "max-width: 420px;\n"
    "box-shadow: 0 16px 40px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.08);\n"
    "text-align: left !important;\n"
    "margin-bottom: 30px;\n"
    "}\n\n"
    "/* GLOBAL STRICT LEFT-ALIGNMENT RULE */\n"
    ".auth-card, .card, .modal, [id$=\"-modal\"], .form-group, #livechat-messages, #livechat-messages div, #onboarding-screen, #auth-screen {\n"
    "  text-align: left !important;\n"
    "}"
)

if old_auth_card_css in content:
    content = content.replace(old_auth_card_css, new_auth_card_css, 1)
    print("SUCCESS 1: Added global strict left-alignment CSS rules")
else:
    print("WARNING 1: Could not find old_auth_card_css, using CRLF byte replacement...")

# 2. Replace all inline `text-align: center;` in auth-card / wizard divs with `text-align: left;`
content = content.replace('class="auth-card" style="text-align: center;', 'class="auth-card" style="text-align: left;')
content = content.replace('style="text-align: center; width: 100%;"', 'style="text-align: left; width: 100%;"')

with open('index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print("File written.")
