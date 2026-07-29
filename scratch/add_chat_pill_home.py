with open('index.html', 'rb') as f:
    content = f.read()

target = (
    b'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">\r\n'
    b'<h3 style="margin: 0;"><span class="k-lbl-en">Cosmic Dashboard</span><span class="k-lbl-hi" style="display:none;">\xe0\xa4\x95\xe0\xa5\x8c\xe0\xa4\xb8\xe0\xa5\x8d\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\x95 \xe0\xa4\xa1\xe0\xa5\x88\xe0\xa4\xb6\xe0\xa4\xac\xe0\xa5\x8b\xe0\xa4\xb0\xe0\xa5\x8d\xe0\xa4\xa1</span></h3>\r\n'
    b'<button class="btn btn-outline" style="width: auto; padding: 6px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.5); color: #c39bd3; display: flex; align-items: center; gap: 6px;" onclick="switchTab(5, document.querySelectorAll(\'.nav-item\')[5])">'
)

replacement = (
    b'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; flex-wrap: wrap; gap: 8px;">\r\n'
    b'<h3 style="margin: 0;"><span class="k-lbl-en">Cosmic Dashboard</span><span class="k-lbl-hi" style="display:none;">\xe0\xa4\x95\xe0\xa5\x8c\xe0\xa4\xb8\xe0\xa5\x8d\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\x95 \xe0\xa4\xa1\xe0\xa5\x88\xe0\xa4\xb6\xe0\xa4\xac\xe0\xa5\x8b\xe0\xa4\xb0\xe0\xa5\x8d\xe0\xa4\xa1</span></h3>\r\n'
    b'<div style="display: flex; gap: 6px; align-items: center;">\r\n'
    b'  <button onclick="openLiveChatModal()" class="btn btn-outline" style="width: auto; padding: 6px 10px; font-size: 0.75rem; border-color: rgba(142, 111, 214, 0.6); color: var(--purple); display: flex; align-items: center; gap: 4px; background: rgba(142, 111, 214, 0.12); cursor: pointer;">\r\n'
    b'    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>\r\n'
    b'    <span>\xef\xbf\xbd Ask AI Assistant</span>\r\n'
    b'  </button>\r\n'
    b'  <button class="btn btn-outline" style="width: auto; padding: 6px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.5); color: #c39bd3; display: flex; align-items: center; gap: 6px;" onclick="switchTab(5, document.querySelectorAll(\'.nav-item\')[5])">'
)

# Let's use simple string find on line 1674 to avoid byte encoding mismatches
with open('index.html', 'rb') as f:
    text_content = f.read().decode('utf-8')

target_str = '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">\r\n<h3 style="margin: 0;"><span class="k-lbl-en">Cosmic Dashboard</span>'

if target_str in text_content:
    new_str = '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; flex-wrap: wrap; gap: 8px;">\r\n<h3 style="margin: 0;"><span class="k-lbl-en">Cosmic Dashboard</span>'
    text_content = text_content.replace(target_str, new_str, 1)
    print("SUCCESS 1: Added flex wrap to Cosmic Dashboard header")

pill_btn_target = '<button class="btn btn-outline" style="width: auto; padding: 6px 12px; font-size: 0.78rem; border-color: rgba(142,111,214,0.5); color: #c39bd3; display: flex; align-items: center; gap: 6px;" onclick="switchTab(5, document.querySelectorAll(\'.nav-item\')[5])">'
pill_btn_replacement = '<button onclick="openLiveChatModal()" class="btn btn-outline" style="width: auto; padding: 5px 10px; font-size: 0.75rem; border-color: rgba(142, 111, 214, 0.6); color: var(--purple); display: flex; align-items: center; gap: 4px; background: rgba(142, 111, 214, 0.15); cursor: pointer; margin-right: 6px;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg><span>Ask AI Assistant</span></button>' + pill_btn_target

if pill_btn_target in text_content:
    text_content = text_content.replace(pill_btn_target, pill_btn_replacement, 1)
    print("SUCCESS 2: Inserted Ask AI Assistant Pill Button")

with open('index.html', 'wb') as f:
    f.write(text_content.encode('utf-8'))

print("File written.")
