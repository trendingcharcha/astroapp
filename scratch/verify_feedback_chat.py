with open('index.html', 'rb') as f:
    content = f.read()

checks = [
    ("1. openFeedbackModal function exists", b"function openFeedbackModal()" in content),
    ("2. submitFeedback function exists", b"async function submitFeedback(e)" in content),
    ("3. selectStarRating function exists", b"function selectStarRating(rating)" in content),
    ("4. openLiveChatModal function exists", b"function openLiveChatModal()" in content),
    ("5. acceptAlternativeTask function exists", b"function acceptAlternativeTask()" in content),
    ("6. Feedback & Chat buttons added to Settings tab", b"APP FEEDBACK & RATING" in content and b"LIVE AI ASSISTANT CHAT" in content),
    ("7. Mandatory feedback fields present in DOM", b"id=\"fb-name\"" in content and b"id=\"fb-email\"" in content and b"id=\"fb-phone\"" in content and b"id=\"fb-profession\"" in content),
    ("8. Supabase insert query present", b"supabaseClient.from('feedbacks').insert" in content),
]

all_pass = True
for title, test in checks:
    status = "PASS" if test else "FAIL"
    if not test: all_pass = False
    print(f"{status}: {title}")

print("\n" + ("ALL FEEDBACK & LIVE CHAT CHECKS PASSED!" if all_pass else "SOME CHECKS FAILED"))
