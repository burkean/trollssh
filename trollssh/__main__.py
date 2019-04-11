import os
import socket
import threading

import paramiko

from trollssh import Server


HOST_KEY = paramiko.RSAKey(filename=os.environ['HOST_KEY'])


def handler(client_sock):
    t = paramiko.Transport(client_sock)
    t.add_server_key(HOST_KEY)

    server = Server()
    t.start_server(server=server)

    chan = t.accept(20)
    if not chan:
        return  # failed auth!


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((os.environ['ADDRESS'], int(os.environ['PORT'])))
    sock.listen(100)

    # with thanks to
    # https://github.com/csinchok/funnypot/blob/243cd09d29f5ee1786aa3dff342e93738c24e6e3/run.py
    connections = []
    while True:
        try:
            conn, addr = sock.accept()
        except InterruptedError:
            break
        except OSError:
            break  # The socket closed...

        try:
            conn.getpeername()[0]
        except OSError:
            conn.close()
            print('Could not get peer name')
            continue

        transport = paramiko.Transport(conn)
        transport.add_server_key(HOST_KEY)
        server = Server()

        event = threading.Event()
        connections.append((transport, event))
        transport.start_server(server=server, event=event)


main()
