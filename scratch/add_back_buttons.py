with open('index.html', 'rb') as f:
    content = f.read().decode('utf-8')

# 1. Feedback Modal Header Replacement
old_fb_header = (
    '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid rgba(232, 200, 121, 0.2); padding-bottom: 10px;">\n'
    '      <h3 style="color: var(--gold); margin: 0; font-size: 1.1rem; display: flex; align-items: center; gap: 8px;">\n'
    '        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>\n'
    '        <span class="k-lbl-en">App Feedback & Rating</span>\n'
    '        <span class="k-lbl-hi" style="display:none;">ऐप प्रतिक्रिया एवं रेटिंग</span>\n'
    '      </h3>\n'
    '      <button class="btn" style="width: auto; padding: 4px 10px; font-size: 0.8rem; background: rgba(255,255,255,0.05);" onclick="closeFeedbackModal()">✕</button>\n'
    '    </div>'
)

new_fb_header = (
    '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid rgba(232, 200, 121, 0.2); padding-bottom: 10px;">\n'
    '      <button onclick="closeFeedbackModal()" class="btn" style="width: auto; padding: 6px 12px; font-size: 0.8rem; background: rgba(232, 200, 121, 0.15); border: 1px solid var(--gold); color: var(--gold); display: flex; align-items: center; gap: 6px; font-weight: bold; cursor: pointer;">\n'
    '        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>\n'
    '        <span class="k-lbl-en">BACK</span><span class="k-lbl-hi" style="display:none;">वापस</span>\n'
    '      </button>\n'
    '      <h3 style="color: var(--gold); margin: 0; font-size: 0.95rem; display: flex; align-items: center; gap: 6px;">\n'
    '        <span class="k-lbl-en">Feedback & Rating</span><span class="k-lbl-hi" style="display:none;">प्रतिक्रिया एवं रेटिंग</span>\n'
    '      </h3>\n'
    '      <button onclick="closeFeedbackModal()" class="btn" style="width: auto; padding: 4px 10px; font-size: 0.9rem; background: rgba(255,255,255,0.1); color: var(--gold); border: 1px solid rgba(232,200,121,0.3); cursor: pointer;" title="Close">✕</button>\n'
    '    </div>'
)

# 2. Live Chat Header Replacement
old_chat_header = (
    '<div style="background: linear-gradient(135deg, rgba(142, 111, 214, 0.25), rgba(12, 9, 34, 0.8)); padding: 14px 18px; border-bottom: 1px solid rgba(142, 111, 214, 0.3); display: flex; justify-content: space-between; align-items: center;">\n'
    '      <div style="display: flex; align-items: center; gap: 10px;">\n'
    '        <div style="width: 38px; height: 38px; border-radius: 50%; background: linear-gradient(135deg, var(--purple), var(--gold)); display: flex; align-items: center; justify-content: center; box-shadow: 0 0 10px rgba(142, 111, 214, 0.5);">\n'
    '          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><path d="M12 2a10 10 0 0 1 10 10c0 5.52-4.48 10-10 10a9.94 9.94 0 0 1-5-1.34L2 22l1.34-5A9.94 9.94 0 0 1 2 12C2 6.48 6.48 2 12 2z"/></svg>\n'
    '        </div>\n'
    '        <div>\n'
    '          <h4 style="margin: 0; color: #fff; font-size: 0.95rem; font-weight: bold;">\n'
    '            <span class="k-lbl-en">AI Karma Assistant</span><span class="k-lbl-hi" style="display:none;">एआई कर्म सहचर</span>\n'
    '          </h4>\n'
    '          <p id="chat-header-sub" style="margin: 0; color: var(--gold); font-size: 0.72rem;">Personalized Task Adapter & Guidance</p>\n'
    '        </div>\n'
    '      </div>\n'
    '      <button class="btn" style="width: auto; padding: 4px 10px; font-size: 0.8rem; background: rgba(255,255,255,0.1);" onclick="closeLiveChatModal()">✕</button>\n'
    '    </div>'
)

new_chat_header = (
    '<div style="background: linear-gradient(135deg, rgba(142, 111, 214, 0.25), rgba(12, 9, 34, 0.8)); padding: 12px 16px; border-bottom: 1px solid rgba(142, 111, 214, 0.3); display: flex; justify-content: space-between; align-items: center;">\n'
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
    '    </div>'
)

if old_fb_header in content:
    content = content.replace(old_fb_header, new_fb_header, 1)
    print("SUCCESS 1: Added BACK button to Feedback Modal Header")
else:
    print("WARNING 1: Could not find old_fb_header")

if old_chat_header in content:
    content = content.replace(old_chat_header, new_chat_header, 1)
    print("SUCCESS 2: Added BACK button to Live Chat Modal Header")
else:
    print("WARNING 2: Could not find old_chat_header")

with open('index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print("File written.")
