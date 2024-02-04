import requests
import json
import time


def can_load_web_socket_debugger_url():
    is_ws_url_set_successfully = False

    url = f"http://127.0.0.1:{ELECTRON_DEBUG_PORT}/json/"

    try:
        response = requests.get(url)
        response.raise_for_status()

        json_data = response.json()

        if isinstance(json_data, list) and len(json_data) > 0:
            web_socket_debugger_url = json_data[0].get("webSocketDebuggerUrl", "")

            if web_socket_debugger_url:
                print(f"The webSocketDebuggerUrl is: {web_socket_debugger_url}")
                ElectronAppSingleton.shared.web_socket_debugger_url_string = web_socket_debugger_url
                is_ws_url_set_successfully = True

    except requests.RequestException as e:
        print(f"Error: {str(e)}")

    wait_maximally_10_seconds()

    return is_ws_url_set_successfully


def wait_maximally_10_seconds():
    start_time = time.time()

    while time.time() - start_time < 10:
        if ElectronAppSingleton.shared.web_socket_debugger_url_string:
            return True
        time.sleep(0.1)

    return False

# Assuming you have defined ELECTRON_DEBUG_PORT and ElectronAppSingleton class elsewhere in your code.
