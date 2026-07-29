with open('index.html', 'rb') as f:
    content = f.read()

# 1. Update restoreProfileFromCloud to avoid overwriting clean local birth details with default fallback strings
old_restore_profile_dob = (
    "localStorage.setItem('user_name', profile.full_name || '');\r\n"
    "localStorage.setItem('kundli_name', profile.full_name || '');\r\n"
    "localStorage.setItem('user_gender', profile.gender || 'M');\r\n"
    "localStorage.setItem('kundli_gender', profile.gender || 'M');\r\n"
    "localStorage.setItem('user_dob', profile.dob || '');\r\n"
    "localStorage.setItem('kundli_date', profile.dob || '');\r\n"
    "localStorage.setItem('user_tob', profile.tob || '');\r\n"
    "localStorage.setItem('kundli_time', profile.tob || '');\r\n"
    "localStorage.setItem('user_pob', profile.pob || '');\r\n"
    "localStorage.setItem('kundli_city', profile.pob || '');"
).encode('utf-8')

new_restore_profile_dob = (
    "if (profile.full_name && profile.full_name !== 'Seeker') {\r\n"
    "  localStorage.setItem('user_name', profile.full_name);\r\n"
    "  localStorage.setItem('kundli_name', profile.full_name);\r\n"
    "}\r\n"
    "if (profile.gender) {\r\n"
    "  localStorage.setItem('user_gender', profile.gender);\r\n"
    "  localStorage.setItem('kundli_gender', profile.gender);\r\n"
    "}\r\n"
    "if (profile.dob && profile.dob !== '1990-01-01') {\r\n"
    "  localStorage.setItem('user_dob', profile.dob);\r\n"
    "  localStorage.setItem('kundli_date', profile.dob);\r\n"
    "}\r\n"
    "if (profile.tob) {\r\n"
    "  localStorage.setItem('user_tob', profile.tob);\r\n"
    "  localStorage.setItem('kundli_time', profile.tob);\r\n"
    "}\r\n"
    "if (profile.pob && profile.pob !== 'New Delhi') {\r\n"
    "  localStorage.setItem('user_pob', profile.pob);\r\n"
    "  localStorage.setItem('kundli_city', profile.pob);\r\n"
    "}"
).encode('utf-8')

# 2. Update generateChart to automatically call syncProfileToCloud() after chart generation
old_genchart_end = (
    "if (typeof drawChart === 'function') drawChart();\r\n"
    "if (typeof renderKundliEnhancedSections === 'function') {\r\n"
    "renderKundliEnhancedSections(placementsList, lagnaSignNum, date);\r\n"
    "}\r\n"
    "if (btn) {\r\n"
    "btn.innerHTML = originalText;\r\n"
    "btn.disabled = false;\r\n"
    "}"
).encode('utf-8')

new_genchart_end = (
    "if (typeof drawChart === 'function') drawChart();\r\n"
    "if (typeof renderKundliEnhancedSections === 'function') {\r\n"
    "renderKundliEnhancedSections(placementsList, lagnaSignNum, date);\r\n"
    "}\r\n"
    "if (typeof syncProfileToCloud === 'function') {\r\n"
    "syncProfileToCloud().catch(err => console.error('Cloud sync error from generateChart:', err));\r\n"
    "}\r\n"
    "if (btn) {\r\n"
    "btn.innerHTML = originalText;\r\n"
    "btn.disabled = false;\r\n"
    "}"
).encode('utf-8')

if old_restore_profile_dob in content:
    content = content.replace(old_restore_profile_dob, new_restore_profile_dob, 1)
    print("SUCCESS 1: Prevented cloud restore from overwriting clean local details with stale fallbacks")
else:
    print("WARNING 1: Could not find old_restore_profile_dob")

if old_genchart_end in content:
    content = content.replace(old_genchart_end, new_genchart_end, 1)
    print("SUCCESS 2: Added syncProfileToCloud to generateChart")
else:
    print("WARNING 2: Could not find old_genchart_end")

with open('index.html', 'wb') as f:
    f.write(content)

print("File written.")
