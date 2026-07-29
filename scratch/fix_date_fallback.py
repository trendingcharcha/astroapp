import re

# Read the file in binary mode to handle CRLF
with open('index.html', 'rb') as f:
    content = f.read()

# The exact pattern from the byte context found above:
# "const parsedT = parseTimeString(time);\r\nhour = parsedT.hour;\r\nmin = parsedT.min;\r\n} catch(e) {\r\nconst now = new Date();\r\n..."
# But we need to find only the ONE at byte 761332 (the generateChart function)
# which is followed shortly by getJulianDay (unlike the minified/Matching variant)

# Full search key with enough distinctive context  
search_context = (
    b"const parsedT = parseTimeString(time);\r\n"
    b"hour = parsedT.hour;\r\n"
    b"min = parsedT.min;\r\n"
    b"} catch(e) {\r\n"
    b"const now = new Date();\r\n"
    b"year = now.getFullYear();\r\n"
    b"month = now.getMonth() + 1;\r\n"
    b"day = now.getDate();\r\n"
    b"hour = now.getHours();\r\n"
    b"min = now.getMinutes();\r\n"
    b"}"
)

replace_context = (
    b"const parsedT = parseTimeString(time);\r\n"
    b"hour = parsedT.hour;\r\n"
    b"min = parsedT.min;\r\n"
    b"} catch(e) {\r\n"
    b"// CRITICAL: Never fallback to today's date for birth data.\r\n"
    b"// Using today's date silently generates a completely wrong Kundli for the user.\r\n"
    b"console.error('[Astro AI] Invalid birth date/time format. Aborting chart generation.', date, time);\r\n"
    b"if (btn) { btn.innerHTML = originalText; btn.disabled = false; }\r\n"
    b"const _chartErrMsg = (typeof currentAppLang !== 'undefined' && currentAppLang === 'hi')\r\n"
    b"? '\\u091c\\u0928\\u094d\\u092e \\u0924\\u093f\\u0925\\u093f \\u092f\\u093e \\u0938\\u092e\\u092f \\u0915\\u093e \\u092a\\u094d\\u0930\\u093e\\u0930\\u0942\\u092a \\u0905\\u092e\\u093e\\u0928\\u094d\\u092f \\u0939\\u0948\\u0964'\r\n"
    b": 'Invalid birth date or time format. Please correct your details.';\r\n"
    b"if (typeof showToast === 'function') showToast(_chartErrMsg, 'error');\r\n"
    b"return; // Abort chart generation\r\n"
    b"}"
)

count = content.count(search_context)
print(f"Found {count} exact matches")

if count == 1:
    content = content.replace(search_context, replace_context, 1)
    print("SUCCESS: Fixed generateChart date fallback bug (never use today's date)")
elif count == 0:
    # Debug - dump context around position 761332
    print("Exact context not found. Dumping actual bytes around that position:")
    pos = 761332
    chunk = content[max(0,pos-100):pos+400]
    print(repr(chunk))
else:
    print(f"Found {count} matches - applying only first (at correct context)")
    content = content.replace(search_context, replace_context, 1)

with open('index.html', 'wb') as f:
    f.write(content)

print("File written.")

# Verify
with open('index.html', 'rb') as f:
    verify = f.read()

if b"Never fallback to today" in verify or b"CRITICAL: Never fallback" in verify:
    print("VERIFICATION PASS: Fix is in file")
else:
    print("VERIFICATION FAIL: Fix not found in file")
