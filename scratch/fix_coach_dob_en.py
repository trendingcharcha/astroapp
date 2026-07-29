with open('index.html', 'rb') as f:
    content = f.read()

# We need to add DOB/POB to the ENGLISH predictionHTML block.
# The English block starts with:
# <p style="margin: 0 0 10px 0;"><strong>Astrological Ascendant (Lagna):</strong> ...
# followed immediately by the Kundli description paragraph.
# We need to insert DOB/POB BETWEEN these two paragraphs.

# Find the exact English marker line in the predictionHTML template
english_marker = (
    b'<p style="margin: 0 0 10px 0;"><strong>Astrological Ascendant (Lagna):</strong>'
    b' <span style="color: var(--gold);">${lagnaName} (${lagnaNameHi})</span>'
    b' | <strong>Ruling Planet:</strong> <span style="color: #5dade2;">${rulingLord}</span></p>\r\n'
)

dob_pob_line = (
    b' <p style="margin: 0 0 8px 0; font-size: 0.85rem; color: var(--text-muted);">'
    b'<strong>Date of Birth:</strong> ${date || \'Unknown\'}'
    b' &nbsp;|&nbsp; <strong>Place of Birth:</strong> ${cityName || \'Unknown\'}</p>\r\n'
)

count = content.count(english_marker)
print(f"English marker found: {count} time(s)")

if count >= 1:
    # Only replace first occurrence (inside generateCoachMission's compileMultiGoalMissionData)
    # Verify the context: it should be followed by "Your horoscope indicates"
    idx = content.find(english_marker)
    after = content[idx + len(english_marker):idx + len(english_marker) + 200]
    print(f"Context after marker: {repr(after[:120])}")
    
    if b'Your horoscope indicates' in after:
        content = content.replace(english_marker, english_marker + dob_pob_line, 1)
        print("SUCCESS: Added English DOB/POB line to predictionHTML")
    else:
        print("WARNING: Context not as expected - checking all occurrences:")
        start = 0
        while True:
            idx = content.find(english_marker, start)
            if idx == -1:
                break
            after = content[idx + len(english_marker):idx + len(english_marker) + 200]
            print(f"  At byte {idx}: {repr(after[:100])}")
            start = idx + 1
else:
    print("Marker not found, debugging...")
    idx = content.find(b'Astrological Ascendant (Lagna):')
    if idx >= 0:
        print(f"Found at byte {idx}:")
        print(repr(content[max(0,idx-50):idx+250]))

with open('index.html', 'wb') as f:
    f.write(content)
print("File written.")

# Verify
with open('index.html', 'rb') as f:
    verify = f.read()

# Count place of birth occurrences in JS template context
pob_count = verify.count(b'Place of Birth')
dob_count = verify.count(b'${date ||')
print(f"'Place of Birth' occurrences in JS: {pob_count}")
print(f"'${{date ||' occurrences: {dob_count}")
