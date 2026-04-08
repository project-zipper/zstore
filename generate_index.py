import os
import json

CUSTOM_APK_DIR = "apks"      # all APKs
ICON_DIR = "icons"           # optional icons folder
OUTPUT_JSON = "index.json"

apps = []

# Walk all APKs recursively
for root, dirs, files in os.walk(CUSTOM_APK_DIR):
    for file in files:
        if file.endswith(".apk"):
            # Full path to APK
            path = os.path.join(root, file).replace("\\", "/")
            # App name
            name = os.path.splitext(file)[0]
            # Category based on folder
            category = os.path.relpath(root, CUSTOM_APK_DIR).replace("\\", "/") or "uncategorized"
            # Optional icon path
            icon_path = f"{ICON_DIR}/{category}/{name}.png"
            apps.append({
                "name": name,
                "package": f"com.zipperos.{name.lower()}",
                "version": "1.0",
                "apk": path,
                "category": category,
                "icon": icon_path
            })

print(f"Total apps found: {len(apps)}")

# Save index.json
with open(OUTPUT_JSON, "w") as f:
    json.dump({"apps": apps}, f, indent=2)

print(f"{OUTPUT_JSON} generated successfully!")
