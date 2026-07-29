with open('index.html', 'rb') as f:
    content = f.read().decode('utf-8')

# 1. Update CSS rule for form-group input, select, textarea
old_css_inputs = (
    ".form-group input, .form-group select {\n"
    "width: 100%;\n"
    "height: 48px;\n"
    "background: var(--input-bg);\n"
    "border: 1px solid var(--input-border);\n"
    "border-radius: 14px;\n"
    "padding: 12px 18px;\n"
    "color: var(--text);\n"
    "font-size: 0.95rem;\n"
    "outline: none;\n"
    "transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);\n"
    "box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);\n"
    "}"
)

new_css_inputs = (
    "*, *::before, *::after {\n"
    "  box-sizing: border-box;\n"
    "}\n\n"
    ".form-group input, .form-group select, .form-group textarea, textarea, input[type=\"text\"], input[type=\"email\"], input[type=\"tel\"], input[type=\"password\"] {\n"
    "  width: 100% !important;\n"
    "  box-sizing: border-box !important;\n"
    "  background: var(--input-bg);\n"
    "  border: 1px solid var(--input-border);\n"
    "  border-radius: 14px;\n"
    "  padding: 12px 18px;\n"
    "  color: var(--text);\n"
    "  font-size: 0.95rem;\n"
    "  font-family: inherit;\n"
    "  outline: none;\n"
    "  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);\n"
    "  box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);\n"
    "}\n\n"
    ".form-group textarea, textarea {\n"
    "  min-height: 90px;\n"
    "  resize: vertical;\n"
    "  line-height: 1.5;\n"
    "}"
)

if old_css_inputs in content:
    content = content.replace(old_css_inputs, new_css_inputs, 1)
    print("SUCCESS 1: Applied global input, textarea, and box-sizing CSS rules")
else:
    print("WARNING 1: Could not find old_css_inputs")

# 2. Update textarea in Feedback Modal for exact alignment
old_fb_textarea = '<textarea id="fb-comments" rows="3" placeholder="Share your experience or suggestions to help us improve..."></textarea>'
new_fb_textarea = '<textarea id="fb-comments" rows="3" placeholder="Share your experience or suggestions to help us improve..." style="width:100% !important; box-sizing:border-box !important; border-radius:14px; padding:12px 18px; font-family:inherit; min-height:95px;"></textarea>'

if old_fb_textarea in content:
    content = content.replace(old_fb_textarea, new_fb_textarea, 1)
    print("SUCCESS 2: Updated Feedback Modal textarea width and box-sizing")
else:
    print("WARNING 2: Could not find old_fb_textarea")

with open('index.html', 'wb') as f:
    f.write(content.encode('utf-8'))

print("File written.")
