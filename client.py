#!/usr/bin/python
import socket
import threading
import time
import os
import sys

def convertNametoIPv6(node_name):
    """
    Takes a node name and translates it to an IPv6 address for
    routing purposes.
    args:
      node_name - string; user friendly name of destination node
    returns:
      IPv6 address of related node
      isValid flag if node name is recognized
    """
    
    if((node_name == "mahia") or (node_name == "MAHIA")):
        return "fdf4:abfb:707:0:38d9:b7d9:8395:21df", True
    else:
        if((node_name == "peace") or (node_name == "PEACE")):
            return "fdf4:abfb:707:0:10:b1e7:8a56:be8", True
        else:
          if((node_name == "king") or (node_name == "KING")):
              return "fdf4:abfb:707:0:c8ad:b3ca:3222:cf90", True
          else:
              return "::1", False

def parseRequest(user_request):
    """
    Takes user input and splits it up into the command,
    node name, and path
    args:
      user_request - string; user inputted statement
    returns:
      command action system is to take
      node_name target node of action
      path location of file
    """
    
    args = user_request.strip().split(' ')
    command = None
    node_name = None
    path = None
    if(len(args) > 0):
        command = args[0]
        if(len(args) > 1):
            node_name = args[1]
            if(len(args) > 2):
                path = args[2]
    return command, node_name, path


def fetch_local_ipv6_address(IP_address, port):
    """
        try to detect whether IPv6 is supported at the present system and
        fetch the IPv6 address of localhost.
    """
    if not socket.has_ipv6:
        raise Exception("the local machine has no IPv6 support enabled")

    addrs = socket.getaddrinfo(IP_address, port, socket.AF_INET6, 0, socket.SOL_TCP)
    # example output: [(23, 0, 6, '', ('::1', 10008, 0, 0))]

    if len(addrs) == 0:
        raise Exception("there is no IPv6 address configured for localhost")

    entry0 = addrs[0]
    sockaddr = entry0[-1]
    return sockaddr

def ReceiveFile(sock, path):
    """
        Receive the file sent by the server to the current directory
    """
    
    pathList = path.split("/")
    filename = pathList[-1]
    if path != "q":
        sock.send(path.encode())
        data = sock.recv(1024).decode()
        print(data[:6])
        if data[:6] == "EXISTS":
            filesize = int(data[6:])
            print(filesize)
            msg = input("File found: " + str(filesize)+ " bytes. Download? (Y?N): ")
            if msg == "Y":
                sock.send("OK".encode())
                # fileToOpen = os.path.join(path)
                f = open("new_" + filename, "wb")
                data = sock.recv(1024).decode()
                totalRecv = len(data)
                print("initial: ", totalRecv, filesize) 
                f.write(data.encode())
                while totalRecv < filesize: # never uses this loop
                    print(totalRecv, filesize)
                    data = sock.recv(1024).decode()
                    totalRecv += len(data)
                    f.write(data.encode())
                    print("{0:.2f}".format((totalRecv/(float)(filesize))*100)+"% done")
                print("Download complete, file ready!")
        else:
            # print("The file you requested does not exist!")
            print("No such file '{}'".format(path), file=sys.stderr)
    
    sock.close()
    
def ipv6_client(sockaddr, path):
    """
        Echo client program
        use hostname or port number or use 'sockaddr' to open the connection

        HOST = 'localhost'
        PORT = 10008, The same port as used by the server
    """
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.connect(sockaddr)

    print("client opened socket connection:", s.getsockname())
    ReceiveFile(s, path)

    
def main():
    print("sample")
    user_input = input('/> ')
    command, node_name, path = parseRequest(user_input)

    if(command != None):
        if(command == "get") or (command == "GET"):
            if(node_name != None) and (path != None):
                try:
                    target_ip, status = convertNametoIPv6(node_name)
                    # fetch the local IPv6 address
                    local_ipv6_addr = fetch_local_ipv6_address(target_ip,10008)
                    '''t = threading.Thread(target=test_server.ipv6_server, args=(local_ipv6_addr,))
                    t.start()'''

                    time.sleep(1)
                    ipv6_client(local_ipv6_addr, path)

                except Exception as e:
                    print("Error occurred: ", e)
            else:
                print("Invalid request. . .", file=sys.stderr)
        else:
            print("Invalid command. . .", file=sys.stderr)
    else:
        print("Invalid input. . .", file=sys.stderr)

    print("Quitting", file=sys.stderr)
    return

main()
