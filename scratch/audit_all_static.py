import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("=== DEEP AUDIT OF ALL CARDS & RENDER FUNCTIONS IN INDEX.HTML ===")

# Find all script blocks
scripts = re.findall(r'<script[\s\S]*?>([\s\S]*?)</script>', html, re.IGNORECASE)

print(f"Total inline script blocks: {len(scripts)}")

# 1. Search for function definitions
funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', html)
print(f"Total JS functions found: {len(funcs)}")

# Filter functions that render UI, populate text, or generate content
render_funcs = [fn for fn in funcs if any(k in fn.lower() for k in ['render', 'generate', 'populate', 'update', 'show', 'calc', 'build'])]
print(f"Render/Population functions found ({len(render_funcs)}):")
for r in render_funcs:
    print(f" - {r}")

# 2. Inspect static elements inside HTML containers or JS defaults
static_patterns = [
    (r'id=["\'](k-[a-zA-Z0-9_-]+)["\']', 'Kundli element IDs'),
    (r'id=["\'](v-[a-zA-Z0-9_-]+)["\']', 'Vastu element IDs'),
    (r'id=["\'](l-[a-zA-Z0-9_-]+)["\']', 'Lal Kitab element IDs'),
    (r'id=["\'](m-[a-zA-Z0-9_-]+)["\']', 'Matching element IDs'),
    (r'id=["\'](c-[a-zA-Z0-9_-]+)["\']', 'Coach element IDs'),
    (r'id=["\'](today_[a-zA-Z0-9_-]+)["\']', 'Today Quest element IDs')
]

print("\n=== DOM ELEMENT IDS CHECK ===")
for pat, label in static_patterns:
    matches = re.findall(pat, html)
    print(f"{label} ({len(matches)}): {matches[:10]}")
