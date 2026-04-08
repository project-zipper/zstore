import os
import json
import requests

# ---------- CONFIG ----------
FDROID_INDEX_URL = "https://f-droid.org/repo/index-v1.json"
CUSTOM_APK_DIR = "apks"      # your custom APKs in repo
ICON_DIR = "icons"           # optional icons folder
FDROID_APK_DIR = "apks/fdroid"  # where to download F-Droid APKs
OUTPUT_JSON = "index.json"
# ----------------------------

os.makedirs(FDROID_APK_DIR, exist_ok=True)

apps = []

# 1️⃣ Load F-Droid metadata
print("Fetching F-Droid index...")
fdroid_data = requests.get(FDROID_INDEX_URL).json()

for pkg, details in fdroid_data["packages"].items():
    latest = details["versions"][-1]
    apk_name = latest["apkName"]
    apk_url = f"https://f-droid.org/repo/{apk_name}"
    local_path = os.path.join(FDROID_APK_DIR, apk_name)

    # Download APK if not already present
    if not os.path.exists(local_path):
        print(f"Downloading {apk_name}...")
        r = requests.get(apk_url)
        with open(local_path, "wb") as f:
            f.write(r.content)

    app_name = details["metadata"]["name"].get("en", pkg)
    apps.append({
        "name": app_name,
        "package": pkg,
        "version": latest["versionName"],
        "apk": local_path.replace("\\","/"),  # local repo path
        "category": details["metadata"].get("categories", ["fdroid"])[0],
        "icon": f"icons/fdroid/{pkg}.png"  # optional
    })

# 2️⃣ Scan custom repo APKs
for root, dirs, files in os.walk(CUSTOM_APK_DIR):
    for file in files:
        if file.endswith(".apk"):
            path = os.path.join(root, file).replace("\\","/")
            name = os.path.splitext(file)[0]
            category = root.split("/")[-1]
            icon_path = f"{ICON_DIR}/{category}/{name}.png"
            apps.append({
                "name": name,
                "package": f"com.zipperos.{name.lower()}",
                "version": "1.0",
                "apk": path,
                "category": category,
                "icon": icon_path
            })

# 3️⃣ Save index.json
with open(OUTPUT_JSON, "w") as f:
    json.dump({"apps": apps}, f, indent=2)

print(f"Generated JSON with {len(apps)} apps!")
