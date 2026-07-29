import re

with open('index.html', 'rb') as f:
    content = f.read().decode('utf-8')

# 1. Update Live Chat Modal Markup to remove top quick selector pills and initialize wizard UI
old_livechat_modal = (
    '<div id="livechat-modal" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(12, 9, 34, 0.95); backdrop-filter: blur(12px); z-index: 100010; align-items: center; justify-content: center; padding: 15px;">\n'
    '  <div class="auth-card" style="max-width: 480px; width: 100%; height: 85vh; border: 1px solid var(--purple); box-shadow: 0 15px 40px rgba(0,0,0,0.9); display: flex; flex-direction: column; padding: 0; overflow: hidden; border-radius: 16px;">\n'
    '    \n'
    '    <!-- Chat Header -->\n'
    '    <div style="background: linear-gradient(135deg, rgba(142, 111, 214, 0.25), rgba(12, 9, 34, 0.8)); padding: 12px 16px; border-bottom: 1px solid rgba(142, 111, 214, 0.3); display: flex; justify-content: space-between; align-items: center;">\n'
    '      <button onclick="closeLiveChatModal()" class="btn" style="width: auto; padding: 6px 12px; font-size: 0.8rem; background: rgba(142, 111, 214, 0.2); border: 1px solid var(--purple); color: var(--purple); display: flex; align-items: center; gap: 6px; font-weight: bold; cursor: pointer;">\n'
    '        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>\n'
    '        <span class="k-lbl-en">BACK</span><span class="k-lbl-hi" style="display:none;">वापस</span>\n'
    '      </button>\n'
    '      <div style="display: flex; align-items: center; gap: 8px;">\n'
    '        <div style="width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, var(--purple), var(--gold)); display: flex; align-items: center; justify-content: center; box-shadow: 0 0 10px rgba(142, 111, 214, 0.5);">\n'
    '          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><path d="M12 2a10 10 0 0 1 10 10c0 5.52-4.48 10-10 10a9.94 9.94 0 0 1-5-1.34L2 22l1.34-5A9.94 9.94 0 0 1 2 12C2 6.48 6.48 2 12 2z"/></svg>\n'
    '        </div>\n'
    '        <h4 style="margin: 0; color: #fff; font-size: 0.9rem; font-weight: bold;">\n'
    '          <span class="k-lbl-en">AI Karma Assistant</span><span class="k-lbl-hi" style="display:none;">एआई कर्म सहचर</span>\n'
    '        </h4>\n'
    '      </div>\n'
    '      <button onclick="closeLiveChatModal()" class="btn" style="width: auto; padding: 4px 10px; font-size: 0.9rem; background: rgba(255,255,255,0.1); color: var(--purple); border: 1px solid rgba(142,111,214,0.4); cursor: pointer;" title="Close">✕</button>\n'
    '    </div>\n'
    '\n'
    '    <!-- Quick Scenario Prompts Carousel -->\n'
    '    <div style="background: rgba(255,255,255,0.02); padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; gap: 8px; overflow-x: auto; white-space: nowrap;">\n'
    '      <button onclick="sendQuickPrompt(\'office\')" class="btn btn-outline" style="padding: 4px 10px; font-size: 0.72rem; border-color: rgba(142,111,214,0.4); color: var(--purple);">🏢 In Office Right Now</button>\n'
    '      <button onclick="sendQuickPrompt(\'time\')" class="btn btn-outline" style="padding: 4px 10px; font-size: 0.72rem; border-color: rgba(232,200,121,0.4); color: var(--gold);">⏰ Missed Time Window</button>\n'
    '      <button onclick="sendQuickPrompt(\'items\')" class="btn btn-outline" style="padding: 4px 10px; font-size: 0.72rem; border-color: rgba(255,255,255,0.3); color: #fff;">🏠 Don\'t Have Items</button>\n'
    '      <button onclick="sendQuickPrompt(\'desk\')" class="btn btn-outline" style="padding: 4px 10px; font-size: 0.72rem; border-color: rgba(46,204,113,0.4); color: #2ecc71;">🧘 Quick Desk Remedy</button>\n'
    '    </div>\n'
    '\n'
    '    <!-- Messages Container -->\n'
    '    <div id="livechat-messages" style="flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; background: rgba(10,8,28,0.6);">\n'
    '      <!-- Messages rendered dynamically -->\n'
    '    </div>'
)

new_livechat_modal = (
    '<div id="livechat-modal" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(12, 9, 34, 0.95); backdrop-filter: blur(12px); z-index: 100010; align-items: center; justify-content: center; padding: 15px;">\n'
    '  <div class="auth-card" style="max-width: 480px; width: 100%; height: 85vh; border: 1px solid var(--purple); box-shadow: 0 15px 40px rgba(0,0,0,0.9); display: flex; flex-direction: column; padding: 0; overflow: hidden; border-radius: 16px;">\n'
    '    \n'
    '    <!-- Clean Header without Top Carousel -->\n'
    '    <div style="background: linear-gradient(135deg, rgba(142, 111, 214, 0.25), rgba(12, 9, 34, 0.8)); padding: 12px 16px; border-bottom: 1px solid rgba(142, 111, 214, 0.3); display: flex; justify-content: space-between; align-items: center;">\n'
    '      <button onclick="closeLiveChatModal()" class="btn" style="width: auto; padding: 6px 12px; font-size: 0.8rem; background: rgba(142, 111, 214, 0.2); border: 1px solid var(--purple); color: var(--purple); display: flex; align-items: center; gap: 6px; font-weight: bold; cursor: pointer;">\n'
    '        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>\n'
    '        <span class="k-lbl-en">BACK</span><span class="k-lbl-hi" style="display:none;">वापस</span>\n'
    '      </button>\n'
    '      <div style="display: flex; align-items: center; gap: 8px;">\n'
    '        <div style="width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, var(--purple), var(--gold)); display: flex; align-items: center; justify-content: center; box-shadow: 0 0 10px rgba(142, 111, 214, 0.5);">\n'
    '          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><path d="M12 2a10 10 0 0 1 10 10c0 5.52-4.48 10-10 10a9.94 9.94 0 0 1-5-1.34L2 22l1.34-5A9.94 9.94 0 0 1 2 12C2 6.48 6.48 2 12 2z"/></svg>\n'
    '        </div>\n'
    '        <h4 style="margin: 0; color: #fff; font-size: 0.9rem; font-weight: bold;">\n'
    '          <span class="k-lbl-en">AI Task Adapter Wizard</span><span class="k-lbl-hi" style="display:none;">एआई कार्य अनुकूलक सहायक</span>\n'
    '        </h4>\n'
    '      </div>\n'
    '      <button onclick="closeLiveChatModal()" class="btn" style="width: auto; padding: 4px 10px; font-size: 0.9rem; background: rgba(255,255,255,0.1); color: var(--purple); border: 1px solid rgba(142,111,214,0.4); cursor: pointer;" title="Close">✕</button>\n'
    '    </div>\n'
    '\n'
    '    <!-- Messages Container -->\n'
    '    <div id="livechat-messages" style="flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; background: rgba(10,8,28,0.6);">\n'
    '      <!-- Messages rendered dynamically by Wizard Engine -->\n'
    '    </div>'
)

if old_livechat_modal in content:
    content = content.replace(old_livechat_modal, new_livechat_modal, 1)
    print("SUCCESS 1: Updated Live Chat Modal markup (Removed top carousel)")
else:
    print("WARNING 1: Could not find old_livechat_modal")

with open('index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print("File 1 written.")
