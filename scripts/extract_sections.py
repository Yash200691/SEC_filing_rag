from pathlib import Path
import re
import json

# ==========================================================
# Paths
# ==========================================================

INPUT_DIR = Path("data/cleaned")
OUTPUT_DIR = Path("data/sections")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================================
# SEC Section Pattern
# ==========================================================

SECTION_PATTERN = re.compile(
    r'(?i)(Item\s+'
    r'(1A|1B|1C|1|2|3|4|5|6|7A|7|8|9A|9B|9C|9|10|11|12|13|14|15)'
    r'\.?)'
)

# ==========================================================
# Find cleaned documents
# ==========================================================

files = list(INPUT_DIR.rglob("*.txt"))

print(f"Found {len(files)} cleaned filings\n")

# ==========================================================
# Process each filing
# ==========================================================

for file in files:

    print("Processing:", file.name)

    with open(file, "r", encoding="utf-8") as f:
        text = f.read()

    matches = list(SECTION_PATTERN.finditer(text))

    if len(matches) == 0:
        print("No sections found")
        continue

    sections = {}

    for i in range(len(matches)):

        start = matches[i].start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        section_text = text[start:end].strip()

        section_name = matches[i].group(1)

        sections[section_name] = section_text

    # Save JSON

    relative = file.relative_to(INPUT_DIR)

    output_file = OUTPUT_DIR / relative.with_suffix(".json")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=4)

print("\nFinished.")