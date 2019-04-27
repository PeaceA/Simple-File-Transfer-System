import socket  
import threading
import time

def fetch_local_ipv6_address(IP_address, port):
    # try to detect whether IPv6 is supported at the present system and
    # fetch the IPv6 address of localhost.
    if not socket.has_ipv6:
        raise Exception("the local machine has no IPv6 support enabled")

    addrs = socket.getaddrinfo(IP_address, port, socket.AF_INET6, 0, socket.SOL_TCP)
    # example output: [(23, 0, 6, '', ('::1', 10008, 0, 0))]

    if len(addrs) == 0:
        raise Exception("there is no IPv6 address configured for localhost")

    entry0 = addrs[0]
    sockaddr = entry0[-1]
    return sockaddr

def ipv6_server(sockaddr):
    # Echo server program
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.bind(sockaddr)
    s.listen(1)
    print ("server opened socket connection:", s, ", address: '%s'" % sockaddr[0])

    time.sleep(1)
    while True:  # answer a single request
        conn, addr = s.accept()
        print("Got connection from", addr)
        # data = conn.recv(1024)
        data = "Response present"
        conn.send(data)
    print("the socket has successfully connected/n")
    conn.close()

def main():
    x = raw_input('Enter ip address:')
    server_socket = fetch_local_ipv6_address(x,10008)
    ipv6_server(server_socket)

main()

