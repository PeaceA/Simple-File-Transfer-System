import socket  
import threading
import time
import os
import sys

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

def SendFile(name, sock):
    """ 
        send the file from the requested path to the client
    """
    filename = (sock.recv(1024)).decode() #receive filename and decode to get str repr
    print("fileName:", filename)
    if os.path.isfile(filename):
        result = "EXISTS " + str(os.path.getsize(filename))
        # print(result)
        sock.send(result.encode()) #send result as bytes
        userResponse = (sock.recv(1024)).decode() #receive userResponse and decode to get str repr
        if userResponse[:2] == "OK":
            with open(filename.encode(), "rb") as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend.decode() != "": #doesn't usually reach
                    bytesToSend = f.read(1024)
                    # print(bytesToSend.decode(), "tick")
                    sock.send(bytesToSend)
    else:
        err_msg = "ERR"
        err_msg_bytes = err_msg.encode()
        sock.send(err_msg_bytes)
        
    sock.close()
    
def ipv6_server(sockaddr):
    """
        Echo server program
    """
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.bind(sockaddr)
    s.listen(1)
    print ("server opened socket connection:", s, ", address: '%s'" % sockaddr[0])

    time.sleep(1)
    while True:  # answer a single request
        conn, addr = s.accept()
        print("Got connection from", addr)
        t = threading.Thread(target=SendFile, args=("sendFileThread", conn))
        t.start()
    t.join()
    print("the socket has successfully connected/n")
    conn.close()


"""
Takes a node name and translates it to an IPv6 address for
routing purposes.
args:
  node_name - string; user friendly name of destination node
returns:
  IPv6 address of related node
  isValid flag if node name is recognized
"""
def convertNametoIPv6(node_name):
    if(node_name == "mahia") or (node_name == "MAHIA"):
        return "fdf4:abfb:707:0:38d9:b7d9:8395:21df", True
    else:
        if(node_name == "peace") or (node_name == "PEACE"):
            return "fdf4:abfb:707:0:10:b1e7:8a56:be8", True
        else:
            if(node_name == "king") or (node_name == "KING"):
                return "fdf4:abfb:707:0:c8ad:b3ca:3222:cf90", True
            else:
                return "::1", False


def main():
    node_name = input('Device name? (peace | mahia | king | test): ')
    # use IPv6:MeshLocalAddress
    node_address, status = convertNametoIPv6(node_name)
    server_socket = fetch_local_ipv6_address(node_address,10008)
    ipv6_server(server_socket)

main()