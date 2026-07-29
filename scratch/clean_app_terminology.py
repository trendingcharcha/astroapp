with open('index.html', 'rb') as f:
    content = f.read().decode('utf-8')

replacements = [
    (
        '<span class="k-lbl-en">AI Task Adapter Wizard</span><span class="k-lbl-hi" style="display:none;">एआई कार्य अनुकूलक सहायक</span>',
        '<span class="k-lbl-en">Karma Assistant</span><span class="k-lbl-hi" style="display:none;">कर्म सहचर</span>'
    ),
    (
        'Namaste <strong>${userName}</strong>! I am your AI Task Adapter.',
        'Namaste <strong>${userName}</strong>! How can I assist your remedies today?'
    ),
    (
        '<span class="k-lbl-en">LIVE AI ASSISTANT CHAT (TASK ADAPTER)</span><span class="k-lbl-hi" style="display:none;">लाइव एआई सहचर चैट (अनुकूलन)</span>',
        '<span class="k-lbl-en">LIVE KARMA ASSISTANT</span><span class="k-lbl-hi" style="display:none;">लाइव कर्म सहचर</span>'
    ),
    (
        '<span class="k-lbl-en">Sanatan Fast &amp; Muhurat Sync</span>',
        '<span class="k-lbl-en">Vedic Alerts &amp; Muhurat</span>'
    ),
    (
        'Ask AI Assistant',
        'Karma Assistant'
    ),
    (
        '<span class="k-lbl-en">App Feedback &amp; Rating</span>',
        '<span class="k-lbl-en">Feedback &amp; Rating</span>'
    )
]

for old_str, new_str in replacements:
    if old_str in content:
        content = content.replace(old_str, new_str)
        print("SUCCESS: Replaced string")
    else:
        print("NOTE: String not found or already replaced")

with open('index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print("File written.")
