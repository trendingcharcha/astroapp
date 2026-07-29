with open('index.html', 'rb') as f:
    content = f.read()

# We need to add DOB and POB lines into the English and Hindi predictionHTML blocks.
# Strategy: find unique markers and inject the new lines right after them.

# === FIX 1: HINDI block ===
# Find the unique line: "<p style="margin: 0 0 10px 0;"><strong>ज्योतिषीय लग्न (Lagna):"
# and add a new DOB/POB paragraph after it (before the next <p> about Kundli).

hindi_lagna_line = b'<p style="margin: 0 0 10px 0;"><strong>\\u091c\\u094d\\u092f\\u094b\\u0924\\u093f\\u0937\\u0940\\u092f \\u0932\\u0917\\u094d\\u0928 (Lagna):'

# Use raw UTF-8 bytes
# "ज्योतिषीय लग्न" in UTF-8
hindi_marker = (
    b'<p style="margin: 0 0 10px 0;"><strong>'
    b'\xe0\xa4\x9c\xe0\xa5\x8d\xe0\xa4\xaf\xe0\xa5\x8b\xe0\xa4\xa4\xe0\xa4\xbf\xe0\xa4\xb7\xe0\xa5\x80\xe0\xa4\xaf \xe0\xa4\xb2\xe0\xa4\x97\xe0\xa5\x8d\xe0\xa4\xa8 (Lagna):'
)

# Full line to find in file (with CRLF at end)
hindi_marker_line = hindi_marker + (
    b'</strong> <span style="color: var(--gold);">${lagnaNameHi} (${lagnaName})</span>'
    b' | <strong>\xe0\xa4\xb6\xe0\xa4\xbe\xe0\xa4\xb8\xe0\xa4\x95 \xe0\xa4\x97\xe0\xa5\x8d\xe0\xa4\xb0\xe0\xa4\xb9:</strong>'
    b' <span style="color: #5dade2;">${rulingLord}</span></p>\r\n'
)

# The line to insert after it (DOB/POB in Hindi)
hindi_dob_pob_line = (
    b' <p style="margin: 0 0 8px 0; font-size: 0.85rem; color: var(--text-muted);">'
    b'<strong>\xe0\xa4\x9c\xe0\xa4\xa8\xe0\xa5\x8d\xe0\xa4\xae \xe0\xa4\xa4\xe0\xa4\xbf\xe0\xa4\xa5\xe0\xa4\xbf:</strong> ${date || \'\xe0\xa4\x85\xe0\xa4\x9c\xe0\xa5\x8d\xe0\xa4\x9e\xe0\xa4\xbe\xe0\xa4\xa4\'}'
    b' &nbsp;|&nbsp; <strong>\xe0\xa4\x9c\xe0\xa4\xa8\xe0\xa5\x8d\xe0\xa4\xae \xe0\xa4\xb8\xe0\xa5\x8d\xe0\xa4\xa5\xe0\xa4\xbe\xe0\xa4\xa8:</strong>'
    b' ${cityName || \'\xe0\xa4\x85\xe0\xa4\x9c\xe0\xa5\x8d\xe0\xa4\x9e\xe0\xa4\xbe\xe0\xa4\xa4\'}</p>\r\n'
)

# Check if DOB line already exists (avoid double-insert)
if b'${date ||' in content and b'\xe0\xa4\x9c\xe0\xa4\xa8\xe0\xa5\x8d\xe0\xa4\xae \xe0\xa4\xa4\xe0\xa4\xbf\xe0\xa4\xa5\xe0\xa4\xbf' in content:
    print("Hindi DOB/POB line already present - skipping Hindi fix")
elif hindi_marker_line in content:
    content = content.replace(hindi_marker_line, hindi_marker_line + hindi_dob_pob_line, 1)
    print("SUCCESS: Added Hindi DOB/POB line to predictionHTML")
else:
    # Debug: try to find the marker
    idx = content.find(b'\xe0\xa4\x9c\xe0\xa5\x8d\xe0\xa4\xaf\xe0\xa5\x8b\xe0\xa4\xa4\xe0\xa4\xbf\xe0\xa4\xb7\xe0\xa5\x80\xe0\xa4\xaf \xe0\xa4\xb2\xe0\xa4\x97\xe0\xa5\x8d\xe0\xa4\xa8 (Lagna):')
    if idx >= 0:
        print(f"Hindi lagna found at byte {idx}. Nearby bytes:")
        print(repr(content[max(0,idx-30):idx+150]))
    else:
        print("FAIL: Hindi lagna marker not found in file")

# === FIX 2: ENGLISH block ===
# Find: <p style="margin: 0 0 10px 0;"><strong>Astrological Ascendant (Lagna):
english_marker_line = (
    b'<p style="margin: 0 0 10px 0;"><strong>Astrological Ascendant (Lagna):</strong>'
    b' <span style="color: var(--gold);">${lagnaName} (${lagnaNameHi})</span>'
    b' | <strong>Ruling Planet:</strong> <span style="color: #5dade2;">${rulingLord}</span></p>\r\n'
)

english_dob_pob_line = (
    b' <p style="margin: 0 0 8px 0; font-size: 0.85rem; color: var(--text-muted);">'
    b'<strong>Date of Birth:</strong> ${date || \'Unknown\'}'
    b' &nbsp;|&nbsp; <strong>Place of Birth:</strong> ${cityName || \'Unknown\'}</p>\r\n'
)

if b'Date of Birth' in content and b'Place of Birth' in content:
    print("English DOB/POB line already present - skipping English fix")
elif english_marker_line in content:
    # Replace only the FIRST occurrence (the one inside generateCoachMission)
    count = content.count(english_marker_line)
    print(f"English marker found {count} time(s)")
    content = content.replace(english_marker_line, english_marker_line + english_dob_pob_line, 1)
    print("SUCCESS: Added English DOB/POB line to predictionHTML")
else:
    idx = content.find(b'Astrological Ascendant (Lagna):')
    if idx >= 0:
        print(f"English lagna found at byte {idx}. Nearby bytes:")
        print(repr(content[max(0,idx-30):idx+200]))
    else:
        print("FAIL: English Ascendant marker not found in file")

with open('index.html', 'wb') as f:
    f.write(content)
print("File written.")

# Verify
with open('index.html', 'rb') as f:
    verify = f.read()
if b'Date of Birth' in verify:
    print("VERIFY OK: English DOB line present")
if b'\xe0\xa4\x9c\xe0\xa4\xa8\xe0\xa5\x8d\xe0\xa4\xae \xe0\xa4\xa4\xe0\xa4\xbf\xe0\xa4\xa5\xe0\xa4\xbf' in verify:
    print("VERIFY OK: Hindi DOB line present")
