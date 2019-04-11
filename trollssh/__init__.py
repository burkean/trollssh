import threading
import time
import random

import paramiko


RED = '\u001b[31m'
GREEN = '\u001b[32m'
BLUE = '\u001b[34m'
YELLOW = '\u001b[33m'
RESET = '\u001b[0m'

FORWARD = '\u001b[1C'


class Server(paramiko.ServerInterface):
    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_interactive(self, username, submethods):
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return 'keyboard-interactive'

    def check_channel_shell_request(self, channel):
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        shell = Shell(channel, width, height)
        shell.start()
        return True


class Shell(threading.Thread):
    def __init__(self, channel, width, height):
        super().__init__()
        self.channel = channel
        self.width = width
        self.height = height

    def run(self):
        self.channel.sendall('\u001b[D\u001b[2J\u001b[0;0H')
        self.channel.sendall("[7mFile Edit Options Buffers Tools Lisp-Interaction Help" + " " * (self.width - 53) + "[0m")

        self.channel.sendall(f'\u001b[{self.height - 1};0H')
        self.channel.sendall("[7m-UUU:----F1  *scratch*      All L1     (Org) ----------------------------------" + " " * (self.width - 79) + "[0m")
        self.channel.sendall(f'\u001b[{self.height};0H')
        self.channel.sendall("For more information about GNU Emacs and the GNU system, type C-h C-a")

        time.sleep(2)
        self.channel.sendall(f'\u001b[2K')
        self.channel.sendall('\u001b[3;0H')
        echo = make_echo(self.channel.sendall)
        echo(BLUE + "* Welcome" + RESET)
        echo("  Hi, you've discovered my SSH Server")
        echo("  There are many like it, but this one is mine.")
        echo("")
        echo(BLUE + "* Work" + RESET)
        echo("  I am a committed UK history teacher.")
        echo("")
        echo(BLUE + "* Contact" + RESET)
        echo("  Drop me an email at " + GREEN + "<tom@hillsdon.net>" + RESET)
        echo("")
        echo(BLUE + "* Quitting" + RESET)
        echo("  I bet you don't know how to exit a hung ssh session.")
        echo("  The question is: will I hang up before you can Google the answer...")
        self.channel.sendall(FORWARD + FORWARD)
        time.sleep(10)
        echo("\r\n  Still here?")
        echo("  Ok, fine: [enter] + ~ + .")
        self.channel.sendall(FORWARD + FORWARD)
        time.sleep(60)
        self.channel.sendall('\u001b[2J\u001b[?25h')
        self.channel.close()


def make_echo(sendall):
    def inner_echo(line):
        for char in line:
            sendall(char)
            time.sleep(random.choices([0.05, 0.1, 0.2, 0.3], [12, 4, 1, 1])[0])
        sendall('\r\n')

    return inner_echo
