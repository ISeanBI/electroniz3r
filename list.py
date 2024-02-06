import os
from pathlib import Path

class ElectronApp:
    def __init__(self, path, identifier):
        self.path = path
        self.identifier = identifier

def list_electron_app_paths():
    electron_framework_subdirectories = []

    def search_for_electron_framework(path, depth):
        if depth > 6:
            return
        try:
            subdirectories = os.listdir(path)
            for subdirectory in subdirectories:
                subdirectory_path = os.path.join(path, subdirectory)
                if os.path.isdir(subdirectory_path):
                    if subdirectory == "Electron Framework.framework":
                        electron_framework_subdirectories.append(subdirectory_path)
                    elif subdirectory_path != "/Applications/Xcode.app":
                        search_for_electron_framework(subdirectory_path, depth + 1)
        except Exception as e:
            print(f"Error: {e}")

    applications_directory_path = ["/Applications"]

    if os.getlogin() != "root":
        user_applications_directory_path = os.path.expanduser("~/Applications")
        applications_directory_path.append(user_applications_directory_path)

    for path in applications_directory_path:
        search_for_electron_framework(path, 0)

    return electron_framework_subdirectories

def list_electron_apps():
    electron_app_paths = list_electron_app_paths()
    electron_apps = []

    for electron_app_path in electron_app_paths:
        electron_framework_url = Path(electron_app_path)
        electron_app_url = electron_framework_url.parent.parent.parent

        try:
            with open(electron_app_url / "Contents" / "Info.plist", "rb") as plist_file:
                plist_data = plist_file.read()
                bundle_identifier = plist_data.decode("utf-8").split("<key>CFBundleIdentifier</key>")[1].split("<string>")[1].split("</string>")[0]

            electron_apps.append(ElectronApp(path=str(electron_app_url), identifier=bundle_identifier))
        except Exception as e:
            print(f"Error reading Info.plist: {e}")

    return electron_apps

def pretty_print_electron_apps():
    electron_apps = list_electron_apps()

    print("╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗")
    print("║    Bundle identifier                      │       Path                                               ║")
    print("╚──────────────────────────────────────────────────────────────────────────────────────────────────────╝")

    for electron_app in electron_apps:
        offset = 45 - len(electron_app.identifier)
        if offset < 0:
            offset = 2

        print(f"{electron_app.identifier}{' ' * offset}{electron_app.path}")

# Uncomment the line below to run the pretty_print_electron_apps function
pretty_print_electron_apps()
