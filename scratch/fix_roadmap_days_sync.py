with open('index.html', 'rb') as f:
    content = f.read()

# 1. Update getPlanStartDayOffset to compute date difference strictly by calendar YYYY-MM-DD days
old_getPlanStartDayOffset = (
    "function getPlanStartDayOffset() {\r\n"
    "let planStartDate = localStorage.getItem('karma_plan_start_date');\r\n"
    "if (!planStartDate) {\r\n"
    "planStartDate = getFormattedDate();\r\n"
    "localStorage.setItem('karma_plan_start_date', planStartDate);\r\n"
    "}\r\n"
    "const startDateObj = new Date(planStartDate);\r\n"
    "const todayObj = new Date();\r\n"
    "const diffTime = Math.abs(todayObj - startDateObj);\r\n"
    "let dayNum = Math.floor(diffTime / (1000 * 60 * 60 * 24)) + 1;\r\n"
    "return Math.min(Math.max(dayNum, 1), 90);\r\n"
    "}"
).encode('utf-8')

new_getPlanStartDayOffset = (
    "function getPlanStartDayOffset() {\r\n"
    "let planStartDate = localStorage.getItem('karma_plan_start_date');\r\n"
    "if (!planStartDate) {\r\n"
    "planStartDate = typeof getFormattedDate === 'function' ? getFormattedDate() : new Date().toISOString().split('T')[0];\r\n"
    "localStorage.setItem('karma_plan_start_date', planStartDate);\r\n"
    "}\r\n"
    "try {\r\n"
    "const sParts = planStartDate.split('-');\r\n"
    "const tStr = typeof getFormattedDate === 'function' ? getFormattedDate() : new Date().toISOString().split('T')[0];\r\n"
    "const tParts = tStr.split('-');\r\n"
    "const startUtc = Date.UTC(parseInt(sParts[0]), parseInt(sParts[1]) - 1, parseInt(sParts[2]));\r\n"
    "const todayUtc = Date.UTC(parseInt(tParts[0]), parseInt(tParts[1]) - 1, parseInt(tParts[2]));\r\n"
    "const diffDays = Math.floor((todayUtc - startUtc) / 86400000) + 1;\r\n"
    "return Math.min(Math.max(diffDays, 1), 90);\r\n"
    "} catch(e) {\r\n"
    "return 1;\r\n"
    "}\r\n"
    "}"
).encode('utf-8')

# 2. Add karma_plan_start_date to syncProfileToCloud activeGoalsPayload
old_cloud_payload_start_date = (
    "user_moon_rashi_idx: localStorage.getItem('user_moon_rashi_idx') || '',\r\n"
    "karma_daily_roadmap_history: localStorage.getItem('karma_daily_roadmap_history') || '{}'"
).encode('utf-8')

new_cloud_payload_start_date = (
    "user_moon_rashi_idx: localStorage.getItem('user_moon_rashi_idx') || '',\r\n"
    "karma_daily_roadmap_history: localStorage.getItem('karma_daily_roadmap_history') || '{}',\r\n"
    "karma_plan_start_date: localStorage.getItem('karma_plan_start_date') || (typeof getFormattedDate === 'function' ? getFormattedDate() : new Date().toISOString().split('T')[0])"
).encode('utf-8')

# 3. Add karma_plan_start_date to restoreProfileFromCloud
old_cloud_restore_start_date = (
    "if (payload.karma_daily_roadmap_history) {\r\n"
    "localStorage.setItem('karma_daily_roadmap_history', typeof payload.karma_daily_roadmap_history === 'string' ? payload.karma_daily_roadmap_history : JSON.stringify(payload.karma_daily_roadmap_history));\r\n"
    "}"
).encode('utf-8')

new_cloud_restore_start_date = (
    "if (payload.karma_daily_roadmap_history) {\r\n"
    "localStorage.setItem('karma_daily_roadmap_history', typeof payload.karma_daily_roadmap_history === 'string' ? payload.karma_daily_roadmap_history : JSON.stringify(payload.karma_daily_roadmap_history));\r\n"
    "}\r\n"
    "if (payload.karma_plan_start_date) {\r\n"
    "localStorage.setItem('karma_plan_start_date', payload.karma_plan_start_date);\r\n"
    "}"
).encode('utf-8')

# Apply replacements
if old_getPlanStartDayOffset in content:
    content = content.replace(old_getPlanStartDayOffset, new_getPlanStartDayOffset, 1)
    print("SUCCESS 1: Updated getPlanStartDayOffset with strict UTC calendar date math")
else:
    print("WARNING 1: Could not find old_getPlanStartDayOffset")

if old_cloud_payload_start_date in content:
    content = content.replace(old_cloud_payload_start_date, new_cloud_payload_start_date, 1)
    print("SUCCESS 2: Added karma_plan_start_date to syncProfileToCloud payload")
else:
    print("WARNING 2: Could not find old_cloud_payload_start_date")

if old_cloud_restore_start_date in content:
    content = content.replace(old_cloud_restore_start_date, new_cloud_restore_start_date, 1)
    print("SUCCESS 3: Added karma_plan_start_date to restoreProfileFromCloud")
else:
    print("WARNING 3: Could not find old_cloud_restore_start_date")

with open('index.html', 'wb') as f:
    f.write(content)

print("File written.")
