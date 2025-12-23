from pathlib import Path

BASE_DIR = Path(__file__).parent

templates_path = BASE_DIR / "templates" / "index.html"
static_path = BASE_DIR / "static" / "style.css"

print("Checking paths...\n")

if templates_path.exists():
    print(f"✅ Found index.html at: {templates_path}")
else:
    print(f"❌ index.html NOT found at: {templates_path}")

if static_path.exists():
    print(f"✅ Found style.css at: {static_path}")
else:
    print(f"❌ style.css NOT found at: {static_path}")

print("\nFolder structure in project root:")
for p in BASE_DIR.iterdir():
    print(f"- {p.name}")
