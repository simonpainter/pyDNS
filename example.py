#!/usr/bin/env python3

#import our modules
from pyDNS import Server
import time

#set server variables
serverIP='127.0.0.1'
serverPort = 53



s=Server()
s.start(serverIP,serverPort)
while 1:
	print("Server running")
	time.sleep(5)
