#!/usr/bin/env python3

#import our modules
import pyDNS
import socket

#set server variables
serverIP=''
serverPORT = 53

#Open the socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((serverIP, serverPORT))

while 1:
	data, addr = sock.recvfrom(512) # buffer size is 512 bytes
	query = data[12:]
	print(query)
