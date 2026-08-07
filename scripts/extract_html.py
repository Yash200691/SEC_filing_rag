from pathlib import Path
import re

# ======================================================
# Paths
# ======================================================

RAW_DATA = Path("data/raw/sec-edgar-filings")
OUTPUT = Path("data/html")

OUTPUT.mkdir(parents=True, exist_ok=True)

# ======================================================
# Find every SEC text file
# ======================================================

files = list(RAW_DATA.rglob("*.txt"))

print(f"Found {len(files)} SEC filings\n")

# ======================================================
# Process every file
# ======================================================

for file in files:

    print("Processing:", file.name)

    with open(file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # --------------------------------------------------
    # Find the HTML inside the TEXT tag
    # --------------------------------------------------

    match = re.search(
        r"<TEXT>(.*?)</TEXT>",
        content,
        re.DOTALL | re.IGNORECASE,
    )

    if not match:
        print("TEXT section not found")
        continue

    html = match.group(1)

    # --------------------------------------------------
    # Find where HTML actually starts
    # --------------------------------------------------

    start = html.find("<html")

    if start != -1:
        html = html[start:]

    # --------------------------------------------------
    # Save HTML
    # --------------------------------------------------

    relative = file.relative_to(RAW_DATA)

    output_file = OUTPUT / relative.with_suffix(".html")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

print("\nDone!")