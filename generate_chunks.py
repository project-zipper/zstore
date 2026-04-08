import json
import math
import os

CHUNK_SIZE = 300  # smaller = smoother loading

INPUT_FILE = "index.json"

# Load main index
if not os.path.exists(INPUT_FILE):
    print("index.json not found!")
    exit(1)

with open(INPUT_FILE, "r") as f:
    data = json.load(f)

apps = data.get("apps", [])

if not apps:
    print("No apps found!")
    exit(1)

def is_placeholder(app):
    return (
        app.get("category") == "placeholders" or
        "placeholder" in app.get("name", "").lower() or
        "placeholder" in app.get("package", "").lower()
    )

# Clean old chunks
for file in os.listdir():
    if file.startswith("index-") and file.endswith(".json"):
        os.remove(file)

chunk_files = []
total_chunks = math.ceil(len(apps) / CHUNK_SIZE)

for i in range(total_chunks):
    chunk_apps = apps[i * CHUNK_SIZE:(i + 1) * CHUNK_SIZE]

    safe_apps = []

    for app in chunk_apps:
        # DO NOT modify ANY app (real or placeholder)
        # Just validate structure
        safe_apps.append({
            "name": app.get("name", "Unknown App"),
            "package": app.get("package", f"com.zipperos.unknown{i}"),
            "version": app.get("version", "1.0"),
            "apk": app.get("apk", ""),
            "category": app.get("category", "misc"),
            "icon": app.get("icon", "icons/default.png")
        })

    filename = f"index-{i+1}.json"

    with open(filename, "w") as f:
        json.dump({"apps": safe_apps}, f, indent=2)

    chunk_files.append(filename)

# Create master list
with open("index-list.json", "w") as f:
    json.dump({"chunks": chunk_files}, f, indent=2)

print(f"✅ Created {total_chunks} chunks")
print(f"✅ Total apps processed: {len(apps)}")
