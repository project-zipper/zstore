import os
import json
import requests

FDROID_INDEX_URL = "https://f-droid.org/repo/index-v1.json"
FDROID_APK_DIR = "apks/fdroid"
os.makedirs(FDROID_APK_DIR, exist_ok=True)

apps = []

print("Fetching F-Droid index...")
fdroid_data = requests.get(FDROID_INDEX_URL).json()

packages = fdroid_data.get("packages", {})

for pkg, details in packages.items():
    versions = details.get("versions", [])
    if not versions:
        continue  # skip apps without versions

    latest = versions[-1]
    apk_name = latest.get("apkName")
    version_name = latest.get("versionName", "1.0")
    if not apk_name:
        continue  # skip if apkName missing

    apk_url = f"https://f-droid.org/repo/{apk_name}"
    local_path = os.path.join(FDROID_APK_DIR, apk_name)

    # Download APK if not present
    if not os.path.exists(local_path):
        print(f"Downloading {apk_name}...")
        r = requests.get(apk_url)
        with open(local_path, "wb") as f:
            f.write(r.content)

    # Get app name safely
    app_name = details.get("metadata", {}).get("name", {}).get("en", pkg)

    # Category fallback
    category = details.get("metadata", {}).get("categories", ["fdroid"])[0]

    apps.append({
        "name": app_name,
        "package": pkg,
        "version": version_name,
        "apk": local_path.replace("\\","/"),
        "category": category,
        "icon": f"icons/fdroid/{pkg}.png"  # optional
    })

print(f"F-Droid apps added: {len(apps)}")
