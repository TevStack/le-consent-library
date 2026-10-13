"""Checks cookie-library.json before it goes live to every client site."""
import json, re, sys

CATEGORIES = {"necessary", "functional", "analytics", "marketing"}
NAME = re.compile(r"^[A-Za-z0-9!#$%&'*+\-.^_`|~]{1,150}$")
errors = []

try:
    data = json.load(open("cookie-library.json", encoding="utf-8"))
except json.JSONDecodeError as e:
    sys.exit(f"cookie-library.json is not valid JSON: {e}")

if not re.fullmatch(r"\d{4}\.\d{2}\.\d{2}(\.\d+)?", str(data.get("version", ""))):
    errors.append('"version" must look like 2026.10.13 (add .1, .2 for several releases in a day)')

processors = data.get("processors", {})
seen = set()
for i, c in enumerate(data.get("cookies", [])):
    where = f"cookies[{i}] ({c.get('name', '?')})"
    if not NAME.match(str(c.get("name", ""))):
        errors.append(f"{where}: invalid name")
    if c.get("name") in seen:
        errors.append(f"{where}: duplicate name")
    seen.add(c.get("name"))
    if c.get("category") not in CATEGORIES:
        errors.append(f"{where}: category must be one of {sorted(CATEGORIES)}")
    for field in ("provider", "duration", "description"):
        if not c.get(field):
            errors.append(f"{where}: missing {field}")
    if c.get("processor") and c["processor"] not in processors:
        errors.append(f"{where}: processor '{c['processor']}' not in processors")

ids = set()
for i, s in enumerate(data.get("sources", [])):
    where = f"sources[{i}] ({s.get('id', '?')})"
    if not s.get("id") or s["id"] in ids:
        errors.append(f"{where}: missing or duplicate id")
    ids.add(s.get("id"))
    if s.get("category") not in CATEGORIES:
        errors.append(f"{where}: category must be one of {sorted(CATEGORIES)}")
    if not s.get("patterns"):
        errors.append(f"{where}: needs at least one pattern")
    if s.get("processor") and s["processor"] not in processors:
        errors.append(f"{where}: processor '{s['processor']}' not in processors")

for key, p in processors.items():
    if not p.get("name") or not p.get("privacy_url", "").startswith("https://"):
        errors.append(f"processors.{key}: needs a name and an https privacy_url")

if errors:
    print("\n".join("✗ " + e for e in errors))
    sys.exit(1)
print(f"✓ v{data['version']}: {len(data['cookies'])} cookies, {len(data['sources'])} sources, {len(processors)} processors")
