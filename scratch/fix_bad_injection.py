import sys

with open('index.html', 'rb') as f:
    content = f.read()

# The bad injected block between line 8579 and 8595
# We need to replace:
#   if (screen) screen.scrollTop = 0;\r\n
#   } catch(e) { ... bad injected code ... }\r\n  (lines 8580-8594)
#   }\r\n
#   }\r\n
# WITH:
#   if (screen) screen.scrollTop = 0;\r\n
#   }\r\n        <- closes if(el)
#   }\r\n        <- closes if(target)
#   }\r\n        <- closes goToStep function

bad_block = (
    b"if (screen) screen.scrollTop = 0;\r\n"
    b"  } catch(e) {\r\n"
    b"    // CRITICAL: Never fallback to today's date for birth data \xe2\x80\x94 that would generate wrong Kundli silently.\r\n"
    b"    // Show a user-visible error and abort chart generation.\r\n"
    b"    console.error('[Astro AI] Invalid date/time format. Chart generation aborted.', e, date, time);\r\n"
    b"    if (btn) { btn.innerHTML = originalText; btn.disabled = false; }\r\n"
    b"    const errMsg = (currentAppLang === 'hi')\r\n"
    b"      ? '\xe0\xa4\x9c\xe0\xa4\xa8\xe0\xa5\x8d\xe0\xa4\xae \xe0\xa4\xa4\xe0\xa4\xbf\xe0\xa4\xa5\xe0\xa4\xbf \xe0\xa4\xaf\xe0\xa4\xbe \xe0\xa4\xb8\xe0\xa4\xae\xe0\xa4\xaf \xe0\xa4\x95\xe0\xa4\xbe \xe0\xa4\xaa\xe0\xa5\x8d\xe0\xa4\xb0\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x82\xe0\xa4\xaa \xe0\xa4\x85\xe0\xa4\xae\xe0\xa4\xbe\xe0\xa4\xa8\xe0\xa5\x8d\xe0\xa4\xaf \xe0\xa4\xb9\xe0\xa5\x88\xe0\xa5\xa4 \xe0\xa4\x95\xe0\xa5\x83\xe0\xa4\xaa\xe0\xa4\xaf\xe0\xa4\xbe \xe0\xa4\xb8\xe0\xa4\xb9\xe0\xa5\x80 \xe0\xa4\xaa\xe0\xa5\x8d\xe0\xa4\xb0\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x82\xe0\xa4\xaa \xe0\xa4\xae\xe0\xa5\x87\xe0\xa4\x82 \xe0\xa4\xa6\xe0\xa4\xb0\xe0\xa5\x8d\xe0\xa4\x9c \xe0\xa4\x95\xe0\xa4\xb0\xe0\xa5\x87\xe0\xa4\x82 (YYYY-MM-DD / HH:MM)\xe0\xa5\xa4'\r\n"
    b"      : 'Invalid birth date or time format. Please enter a valid date (YYYY-MM-DD) and time (HH:MM).';\r\n"
    b"    if (typeof showToast === 'function') showToast(errMsg, 'error');\r\n"
    b"    return; // Abort \xe2\x80\x94 do NOT generate chart with wrong data\r\n"
    b"  } suggestionsDiv = document.getElementById('onboarding-city-suggestions');\r\n"
    b"if (query.trim().length < 3) {\r\n"
    b"suggestionsDiv.style.display = 'none';\r\n"
    b"return;\r\n"
    b"}\r\n"
    b"}\r\n"
    b"}\r\n"
)

good_block = (
    b"if (screen) screen.scrollTop = 0;\r\n"
    b"}\r\n"   # closes if (el)
    b"}\r\n"   # closes if (target)
    b"}\r\n"   # closes goToStep function
)

count = content.count(bad_block)
print(f"Bad block matches: {count}")

if count == 1:
    content = content.replace(bad_block, good_block, 1)
    print("SUCCESS: Removed bad injection, restored proper closing braces")
else:
    print("Not found - trying byte-level search...")
    # Search for the unique marker line
    marker = b"  } suggestionsDiv = document.getElementById('onboarding-city-suggestions');\r\n"
    idx = content.find(marker)
    if idx >= 0:
        # Find start of the bad block (go back to find "} catch(e)")
        catch_marker = b"  } catch(e) {\r\n    // CRITICAL: Never fallback to today"
        catch_idx = content.rfind(catch_marker, 0, idx)
        if catch_idx >= 0:
            print(f"Found catch block at byte {catch_idx}, marker at {idx}")
            # Find what comes after the bad block
            after_idx = idx + len(marker)
            # The next lines should be "if (query..." then "}" "}" then onboardingSelectedCity
            # We want to find the end of the bad block and cut it out
            # Show what we're cutting
            print("Bytes being cut:", repr(content[catch_idx:idx+200]))

with open('index.html', 'wb') as f:
    f.write(content)

print("File written.")

# Verify
with open('index.html', 'rb') as f:
    verify = f.read()

marker_check = b"suggestionsDiv = document.getElementById('onboarding-city-suggestions');"
if marker_check in verify:
    # Find all occurrences
    idx = 0
    occurrences = []
    while True:
        idx = verify.find(marker_check, idx)
        if idx == -1:
            break
        occurrences.append(idx)
        idx += 1
    print(f"suggestionsDiv occurrences: {len(occurrences)} at bytes {occurrences}")
else:
    print("Good: the bad injection marker is gone")
    
# Confirm the closing structure is correct around old line 8579
if b"if (screen) screen.scrollTop = 0;\r\n}\r\n}\r\n}\r\n" in verify:
    print("STRUCTURE OK: proper triple-close braces present after scrollTop")
