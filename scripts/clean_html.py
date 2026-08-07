from pathlib import Path
from bs4 import BeautifulSoup
import re

# ==========================================================
# Paths
# ==========================================================

HTML_DIR = Path("data/html")
OUTPUT_DIR = Path("data/cleaned")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# Find all html files
# ==========================================================

files = list(HTML_DIR.rglob("*.html"))

print(f"Found {len(files)} HTML files\n")

# ==========================================================
# Process every file
# ==========================================================

for file in files:

    print("Cleaning:", file.name)

    with open(file, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    # ======================================================
    # Parse HTML
    # ======================================================

    soup = BeautifulSoup(html, "lxml")

    # ======================================================
    # Remove unwanted tags
    # ======================================================

    remove_tags = [
        "script",
        "style",
        "meta",
        "link",
        "noscript",
        "svg",
    ]

    for tag in remove_tags:
        for element in soup.find_all(tag):
            element.decompose()

    # ======================================================
    # Remove Inline XBRL tags
    # ======================================================

    xbrl_prefixes = [
        "ix:",
        "xbrli:",
        "link:",
        "dei:",
        "xbrldi:",
        "us-gaap:",
        "ixt:",
    ]

    for tag in soup.find_all():

        name = tag.name.lower()

        if any(name.startswith(prefix) for prefix in xbrl_prefixes):
            tag.decompose()

    # ======================================================
    # Extract visible text
    # ======================================================

    text = soup.get_text(separator="\n")

    # ======================================================
    # Remove blank lines
    # ======================================================

    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # ======================================================
    # Remove extra spaces
    # ======================================================

    text = re.sub(r"[ \t]+", " ", text)

    text = text.strip()

    # ======================================================
    # Save cleaned text
    # ======================================================

    relative = file.relative_to(HTML_DIR)

    output = OUTPUT_DIR / relative.with_suffix(".txt")

    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "w", encoding="utf-8") as f:
        f.write(text)

print("\nFinished Cleaning.")