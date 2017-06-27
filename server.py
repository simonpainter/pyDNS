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



#loop through the query and the reply
while 1:
    data, addr = sock.recvfrom(512) # buffer size is 512 bytes
    header=data[:12]
    question = data[12:]
    ID,QR,Opcode,AA,TC,RD,RA,Z,RCODE,QDCOUNT,ANCOUNT,NSCOUNT,ARCOUNT=pyDNS.parseheader(header)
    QNAME,QTYPE,QCLASS = parsequestion(question)
