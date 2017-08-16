#!/usr/bin/env python3

#import our modules
from pyDNS import Query
import socket

#set server variables
serverIP='127.0.0.1'
serverPORT = 53

#Open the socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((serverIP, serverPORT))



#loop through the query and the reply
while 1:
    data, addr = sock.recvfrom(512) # buffer size is 512 bytes
    Q = Query(data)
    sock.sendto(Q.response(), addr)
