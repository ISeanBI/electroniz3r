import subprocess
import socket
import struct
import time
import os

ELECTRON_DEBUG_PORT = 9222

class ElectronAppSingleton:
    shared = None

    def __init__(self):
        self.pid = None

    def isFinishedLaunching(self):
        return True if self.pid else False

def launchApplicationWithInspectArgument(path):
    openConfiguration = []
    openConfiguration.append("--inspect={}".format(ELECTRON_DEBUG_PORT))

    try:
        subprocess.Popen(["open", "-a", path, "--args"] + openConfiguration)
    except Exception as e:
        print("Error launching application:", e)

def isPortOpen(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", port))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()

def waitMaximally10Seconds(callback):
    max_time = 10
    start_time = time.time()
    while time.time() - start_time < max_time:
        if callback():
            return True
        time.sleep(0.1)
    return False

def isVulnerable(path):
    vulnerableStatus = False

    if isPortOpen(ELECTRON_DEBUG_PORT):
        print("Error: Something already listens on debug port -", ELECTRON_DEBUG_PORT)
        print("-> check it with `lsof -i tcp:{}`".format(ELECTRON_DEBUG_PORT))
        return vulnerableStatus

    launchApplicationWithInspectArgument(path)

    def checkFinishedLaunching():
        return ElectronAppSingleton.shared.isFinishedLaunching() and isPortOpen(ELECTRON_DEBUG_PORT)

    if waitMaximally10Seconds(checkFinishedLaunching):
        print("{} started the debug WebSocket server".format(path))
        vulnerableStatus = True

    return vulnerableStatus