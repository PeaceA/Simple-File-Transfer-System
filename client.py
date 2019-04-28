#!/usr/bin/python
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import socket
import threading
import time
import os
import sys

password = "MPM2019"

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
      paths locations of files
    """

    args = user_request.strip().split(' ')
    command = None
    node_name = None
    paths = None
    if (len(args) > 0):
        command = args[0]
        if (len(args) > 1):
            node_name = args[1]
            if (len(args) > 2):
                paths = args[2:]
    return command, node_name, paths

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
    
def decryption(encryptedString):
	PADDING = '{'
	DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
	#Key is FROM the printout of 'secret' in encryption
	#below is the encryption.
	encryption = encryptedString
	key = ''
	cipher = AES.new(key)
	decoded = DecodeAES(cipher, encryption)
	print (decoded)
    return decoded
    
def decrypt(key, filename):
    chunksize = 64*1024
    outputfile = "decrypted_" + filename[11:]
    
    with open(filename, "rb") as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)
        
        decryptor = AES.new(key, AES.MODE_CBC, IV)
        
        with open(outputfile, "wb") as outfile:
            while True:
                chunk = infile.read(chunksize)
                
                if len(chunk) == 0:
                    break
                
                outfile.write(decryptor.decrypt(chunk))
                
            outfile.truncate(filesize)

def getKey(password):
    hasher = SHA256.new(password.encode())
    return hasher.digest()
    
    
def ReceiveFile(sock, path):
    """
        Receive the file sent by the server to the current directory
    """
    
    pathList = path.split("/")
    filename = pathList[-1]
    decrypt(getKey(password), filename)
    if path != "q":
        sock.send(path.encode())
        data = sock.recv(1024).decode()
        # print(data[:6])
        if data[:6] == "EXISTS":
            filesize = int(data[6:])
            # print(filesize)
            cur_time = time.time()
            sock.send("OK".encode())
            # fileToOpen = os.path.join(path)
            f = open("new_" + filename, "wb")
        
            data = sock.recv(1024).decode()
            totalRecv = len(data)
            # print("initial: ", totalRecv, filesize)
           
            f.write(data.encode())
            while totalRecv < filesize: # never uses this loop
                # print(totalRecv, filesize)
                data = sock.recv(1024).decode()
                totalRecv += len(data)
                f.write(data.encode())
                print("{0:.2f}".format((totalRecv/(float)(filesize))*100)+"% done")
            print("Download complete, file ready!")
            final_time = time.time()
            #round trip time
            rtt = str(final_time-cur_time)
            print("> [" + path + "]" + " Round trip time is " + rtt + " seconds")
        else:
            # print("The file you requested does not exist!")
            print("No such file '{}'".format(path), file=sys.stderr)
    
    sock.close()


def ipv6_client(sockaddr, paths, path_counter):
    """
        Echo client program
        use hostname or port number or use 'sockaddr' to open the connection

        HOST = 'localhost'
        PORT = 10008, The same port as used by the server
    """
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.connect(sockaddr)

    print("client opened socket connection:", s.getsockname())
    ReceiveFile(s, paths[path_counter])

    
def main():
    # print("sample")
    user_input = input('/> ')
    command, node_name, paths = parseRequest(user_input)

    if(command != None):
        if(command == "get") or (command == "GET"):
            if(node_name != None) and (paths != None):
                try:
                    target_ip, status = convertNametoIPv6(node_name)
                    # fetch the local IPv6 address
                    local_ipv6_addr = fetch_local_ipv6_address(target_ip,10008)
                    path_counter = 0
                    while path_counter < len(paths):
                        t = threading.Thread(target=ipv6_client, args=(local_ipv6_addr,paths,path_counter))
                        t.start()
                        path_counter += 1
                    t.join()

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
