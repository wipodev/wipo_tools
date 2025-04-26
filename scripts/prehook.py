# scripts/prehook.py

import re
import sys

SETUP_FILE = "setup_version.txt"

def update_setup_version_file(version: str):
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version)
    if not match:
        print("❌ Versión inválida:", version)
        return 1

    major, minor, patch = match.groups()
    version_str = f"{major}.{minor}.{patch}"
    version_tuple = f"({major}, {minor}, {patch}, 0)"

    with open(SETUP_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if "FileVersion" in line:
            line = re.sub(r"'FileVersion',\s*'[^']+'", f"'FileVersion', '{version_str}'", line)
        elif "ProductVersion" in line:
            line = re.sub(r"'ProductVersion',\s*'[^']+'", f"'ProductVersion', '{version_str}'", line)
        elif "filevers=" in line:
            line = re.sub(r"filevers=\([^)]+\)", f"filevers={version_tuple}", line)
        elif "prodvers=" in line:
            line = re.sub(r"prodvers=\([^)]+\)", f"prodvers={version_tuple}", line)
        new_lines.append(line)

    with open(SETUP_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"✔ setup_version.txt actualizado a {version_str}")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Falta la nueva versión como argumento")
        sys.exit(1)
    sys.exit(update_setup_version_file(sys.argv[1]))
