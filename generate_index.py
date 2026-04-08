import os
import json
import requests

# ---------- CONFIG ----------
FDROID_INDEX_URL = "https://f-droid.org/repo/index-v1.json"
FDROID_APK_DIR = "apks/fdroid"
CUSTOM_APK_DIR = "apks"      # your custom APKs
ICON_DIR = "icons"           # optional icons folder
OUTPUT_JSON = "index.json"
# ----------------------------

os.makedirs(FDROID_APK_DIR, exist_ok=True)

apps = []

# 1️⃣ Fetch F-Droid index
print("Fetching F-Droid index...")
fdroid_data = requests.get(FDROID_INDEX_URL).json()
packages = fdroid_data.get("packages", {})

# Handle packages as dict or list
if isinstance(packages, dict):
    package_items = packages.items()
elif isinstance(packages, list):
    package_items = []
    for item in packages:
        pkg_name = item.get("packageName") or item.get("package") or "unknown"
        package_items.append((pkg_name, item))
else:
    package_items = []

for pkg, details in package_items:
    # Ensure 'versions' exists and is a list
    versions = details.get("versions") if isinstance(details, dict) else []
    if not versions:
        continue

    latest = versions[-1]
    apk_name = latest.get("apkName")
    version_name = latest.get("versionName", "1.0")
    if not apk_name:
        continue

    apk_url = f"https://f-droid.org/repo/{apk_name}"
    local_path = os.path.join(FDROID_APK_DIR, apk_name)

    # Download APK if not already present
    if not os.path.exists(local_path):
        print(f"Downloading {apk_name}...")
        r = requests.get(apk_url)
        with open(local_path, "wb") as f:
            f.write(r.content)

    # Safe fallback for name and category
    metadata = details.get("metadata", {}) if isinstance(details, dict) else {}
    app_name = metadata.get("name", {}).get("en", pkg)
    category = metadata.get("categories", ["fdroid"])[0]

    apps.append({
        "name": app_name,
        "package": pkg,
        "version": version_name,
        "apk": local_path.replace("\\","/"),
        "category": category,
        "icon": f"{ICON_DIR}/fdroid/{pkg}.png"  # optional
    })

print(f"F-Droid apps added: {len(apps)}")

# 2️⃣ Scan custom APKs in repo
for root, dirs, files in os.walk(CUSTOM_APK_DIR):
    for file in files:
        if file.endswith(".apk") and not root.endswith("fdroid"):
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

print(f"Total apps (F-Droid + custom): {len(apps)}")

# 3️⃣ Save index.json
with open(OUTPUT_JSON, "w") as f:
    json.dump({"apps": apps}, f, indent=2)

print(f"Generated {OUTPUT_JSON} successfully!")
