"""A set of libraries that are useful to both the proxy and regular servers."""

# This code uses Python 2.7. These imports make the 2.7 code feel a lot closer
# to Python 3. (They're also good changes to the language!)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# THe Python socket API is based closely on the Berkeley sockets API which
# was originally written for the C programming language.
#
# https://en.wikipedia.org/wiki/Berkeley_sockets
#
# The API is more flexible than you need, and it does some quirky things to
# provide that flexibility. I recommend tutorials instead of complete
# descriptions because those can skip the archaic bits. (The API was released
# more than 35 years ago!)
import socket

import time

# Read this many bytes at a time of a command. Each socket holds a buffer of
# data that comes in. If the buffer fills up before you can read it then TCP
# will slow down transmission so you can keep up. We expect that most commands
# will be shorter than this.
COMMAND_BUFFER_SIZE = 256
HOST = '127.0.0.1'  # localhost address

def CreateServerSocket(port):
    """Creates a socket that listens on a specified port.
    Args:
      port: int from 0 to 2^16. Low numbered ports have defined purposes. Almost
          all predefined ports represent insecure protocols that have died out.
    Returns:
      An socket that implements TCP/IP.
    """

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((HOST,port))
    return server_sock




def ConnectClientToServer(server_sock):
    """Connects client to server.
    Returns:
      A new socket representing the client connection, as well as a tuple holding
      the address of the client
    """

    # Wait until a client connects and then get a socket that connects to the
    # client.

    server_sock.listen()
    return server_sock.accept()


def CreateClientSocket(server_addr, port):
    """Creates a socket that connects to a port on a server."""

    transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transfer_socket.connect((server_addr, port))
    return transfer_socket


def ReadCommand(sock):
    """Read a single command from a socket. The command must end in newline."""

    command_line = sock.recv(COMMAND_BUFFER_SIZE).decode() # ~~~adjust for commands bigger than buffer
    return command_line

def ParseCommand(command):
    """Parses a command and returns the command name, first arg, and remainder.
    All commands are of the form:
        COMMAND arg1 remaining text is called remainder
    Spaces separate the sections, but the remainder can contain additional spaces.
    The returned values are strings if the values are present or `None`. Trailing
    whitespace is removed.
    Args:
      command: string command.
    Returns:
      command, arg1, remainder. Each of these can be None.
    """

    args = command.strip().split(' ')
    command = None
    if args:
        command = args[0]
    arg1 = None
    if len(args) > 1:
        arg1 = args[1]
    remainder = None
    if len(args) > 2:
        remainder = ' '.join(args[2:])
    return command, arg1, remainder




