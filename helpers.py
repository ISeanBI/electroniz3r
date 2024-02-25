import subprocess
import time
import base64
import os

# Constants
ELECTRON_DEBUG_PORT = 13337


# ElectronApp equivalent in Python
class ElectronApp:
    def __init__(self, path, identifier):
        self.path = path
        self.identifier = identifier


# ElectronAppSingleton equivalent in Python
class ElectronAppSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ElectronAppSingleton, cls).__new__(cls)
            cls._instance.pid = 0
            cls._instance.web_socket_debugger_url_string = ""
        return cls._instance

    def is_finished_launching(self):
        # This would require a platform-specific implementation, e.g., using psutil
        pass


# String extension methods equivalent in Python
def color_string(s, color_code):
    return f"\033[{color_code}m{s}\033[0m"


def to_base64(s):
    return base64.b64encode(s.encode()).decode()


# waitMaximally10Seconds equivalent in Python
def wait_maximally_10_seconds(my_block):
    start = time.time()
    while time.time() - start < 10:
        if my_block():
            break


# executeCode equivalent in Python
# Note: This would require a specific implementation to connect and execute code in an Electron app
def execute_code(code):
    pass


# prepareSwiftSelfieTaker equivalent in Python
def prepare_swift_selfie_taker(swift_selfie_taker_b64_executable):
    try:
        swift_selfie_taker_data = base64.b64decode(swift_selfie_taker_b64_executable)
        swift_selfie_taker_path = "/private/tmp/SwiftSelfieTaker"
        with open(swift_selfie_taker_path, "wb") as file:
            file.write(swift_selfie_taker_data)

        # Make the file executable
        os.chmod(swift_selfie_taker_path, os.stat(swift_selfie_taker_path).st_mode | 0o111)
    except Exception as e:
        print(f"Error: {e}")
        exit(-1)
