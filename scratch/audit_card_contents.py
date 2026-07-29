import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("=== SEARCHING FOR POTENTIAL STATIC PLACEHOLDER TEXT IN CARDS ===")

# Look for hardcoded numbers or static text in HTML card elements
card_blocks = re.findall(r'<div[^>]*class=["\'][^"\']*(?:card|box|panel|tile|blueprint|section|widget)[^"\']*["\'][^>]*>([\s\S]*?)</div>', html, re.IGNORECASE)

print(f"Total card containers found in HTML: {len(card_blocks)}")

# Search for any remaining static percentages, dates, or specific names inside card HTML
static_suspects = []

for idx, block in enumerate(card_blocks):
    # Check if block contains text node that looks like hardcoded stats e.g. "85%", "Phase 1:", "John", "1995", etc.
    # ignoring inputs/options
    clean_block = re.sub(r'<(input|select|option|button|script|style)[^>]*>[\s\S]*?</\1>', '', block, flags=re.IGNORECASE)
    clean_text = re.sub(r'<[^>]+>', ' ', clean_block).strip()
    
    if len(clean_text) > 10 and not any(k in block for k in ['id="', 'class="k-lbl-', 'class="k-val-']):
        # Card with text but might be missing dynamic ID
        static_suspects.append((idx, clean_text[:120]))

print(f"\nFound {len(static_suspects)} card container(s) that might contain static text without dynamic IDs:")
for i, (idx, txt) in enumerate(static_suspects[:20]):
    print(f"[{i+1}] Card {idx}: {txt}...")
