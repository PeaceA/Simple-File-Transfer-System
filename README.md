# Simple-File-Transfer-System

**Group Members**
* Peace Aku
* Matthew King
* Mahia Tasneem


**Project Description**
>This project showcases the concept of client/server architecture via socket programming. The devices used for this project are raspberry pis running linux os with each device as part of a mesh network running on openthread. Each device should has  a multithreaded server and a client program which allows for file request and response. Since openthread only permits the use of ipv6, all of the socket communication between devices will be ipv6.


**Requirements Met**
* Implement the installation of Linux OS and Openthread, and setting up the mesh network on Raspberry Pi
* Implement a server and client file transfer application on each device using IPv6  connection. Once connected to the client using telnet, a user should be able to specify the file path of the document being requested from the server. The server on receiving this request should return the file requested by the client. If this file is not found, an appropriate error message should be displayed.
* Implement a functionality to display the round trip time of each file request.


**Instructions for Use**
1. Log into the raspi units using the default username and password (Username: pi Password: raspberry).
1. Navigate to the 'SimpleFileTransfer' folder.
1. Run the desired programs (Server: server.py | Client: client.py).


**As server**
1. Enter the device you are using (NOTE: 1 dot = peace | 2 dot = king | 3 dot = mahia).
1. Press ^C to exit.


**As client**
1. Enter the command with the following parameters <command> <target> <file list>.
1. In this instance <command> will always be 'get', <target> will be peace, king, or mahia, and <file list> will be a series of file paths separated by spaces.
1. Program automatically terminates upon completion.
