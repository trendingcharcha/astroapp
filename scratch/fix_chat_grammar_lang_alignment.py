import re

with open('index.html', 'rb') as f:
    content = f.read().decode('utf-8')

# 1. Add Language Toggle Button to Karma Assistant Chat Header
old_chat_header_right = '<button onclick="closeLiveChatModal()" class="btn" style="width: auto; padding: 4px 10px; font-size: 0.9rem; background: rgba(255,255,255,0.1); color: var(--purple); border: 1px solid rgba(142,111,214,0.4); cursor: pointer;" title="Close">✕</button>'

new_chat_header_right = '''<div style="display: flex; align-items: center; gap: 6px;">
        <button onclick="toggleAppLanguage()" class="lang-toggle-btn" style="background: rgba(240, 215, 123, 0.15); border: 1px solid rgba(240, 215, 123, 0.4); color: var(--gold); padding: 4px 8px; border-radius: 14px; font-size: 0.72rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 4px; backdrop-filter: blur(10px);">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
          <span class="app-lang-label">EN / हिंदी</span>
        </button>
        <button onclick="closeLiveChatModal()" class="btn" style="width: auto; padding: 4px 10px; font-size: 0.9rem; background: rgba(255,255,255,0.1); color: var(--purple); border: 1px solid rgba(142,111,214,0.4); cursor: pointer;" title="Close">✕</button>
      </div>'''

if old_chat_header_right in content:
    content = content.replace(old_chat_header_right, new_chat_header_right, 1)
    print("SUCCESS 1: Added Language Toggle Button to Chat Header")
else:
    print("WARNING 1: Could not find old_chat_header_right")

# 2. Add CSS rule to guarantee left-alignment on all wizard buttons
old_global_left_css = (
    "/* GLOBAL STRICT LEFT-ALIGNMENT RULE */\n"
    ".auth-card, .card, .modal, [id$=\"-modal\"], .form-group, #livechat-messages, #livechat-messages div, #onboarding-screen, #auth-screen {\n"
    "  text-align: left !important;\n"
    "}"
)

new_global_left_css = (
    "/* GLOBAL STRICT LEFT-ALIGNMENT RULE */\n"
    ".auth-card, .card, .modal, [id$=\"-modal\"], .form-group, #livechat-messages, #livechat-messages div, #onboarding-screen, #auth-screen {\n"
    "  text-align: left !important;\n"
    "}\n\n"
    "#livechat-messages button, #livechat-messages .btn, #livechat-messages .btn-outline {\n"
    "  text-align: left !important;\n"
    "  justify-content: flex-start !important;\n"
    "  display: flex !important;\n"
    "  align-items: center !important;\n"
    "  width: 100% !important;\n"
    "  box-sizing: border-box !important;\n"
    "}"
)

if old_global_left_css in content:
    content = content.replace(old_global_left_css, new_global_left_css, 1)
    print("SUCCESS 2: Added strict button left-alignment CSS rules")
else:
    print("WARNING 2: Could not find old_global_left_css, using CRLF byte replacement...")

with open('index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print("File 1 written.")
