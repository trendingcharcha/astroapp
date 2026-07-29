with open('index.html', 'rb') as f:
    content = f.read()

target = (
    b".form-group input, .form-group select {\r\n"
    b"width: 100%;\r\n"
    b"height: 48px;\r\n"
    b"background: var(--input-bg);\r\n"
    b"border: 1px solid var(--input-border);\r\n"
    b"border-radius: 14px;\r\n"
    b"padding: 12px 18px;\r\n"
    b"color: var(--text);\r\n"
    b"font-size: 0.95rem;\r\n"
    b"outline: none;\r\n"
    b"transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);\r\n"
    b"box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);\r\n"
    b"}"
)

replacement = (
    b"*, *::before, *::after {\r\n"
    b"  box-sizing: border-box;\r\n"
    b"}\r\n\r\n"
    b".form-group input, .form-group select, .form-group textarea, textarea, input[type=\"text\"], input[type=\"email\"], input[type=\"tel\"], input[type=\"password\"] {\r\n"
    b"  width: 100% !important;\r\n"
    b"  box-sizing: border-box !important;\r\n"
    b"  background: var(--input-bg);\r\n"
    b"  border: 1px solid var(--input-border);\r\n"
    b"  border-radius: 14px;\r\n"
    b"  padding: 12px 18px;\r\n"
    b"  color: var(--text);\r\n"
    b"  font-size: 0.95rem;\r\n"
    b"  font-family: inherit;\r\n"
    b"  outline: none;\r\n"
    b"  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);\r\n"
    b"  box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);\r\n"
    b"}\r\n\r\n"
    b".form-group textarea, textarea {\r\n"
    b"  min-height: 95px;\r\n"
    b"  resize: vertical;\r\n"
    b"  line-height: 1.5;\r\n"
    b"}"
)

if target in content:
    content = content.replace(target, replacement, 1)
    print("SUCCESS: Added global input, textarea, and box-sizing CSS rules")
else:
    print("WARNING: target not found")

with open('index.html', 'wb') as f:
    f.write(content)

print("File written.")
