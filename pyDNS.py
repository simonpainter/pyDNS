import socket
import threading
import time

class Server:
	def __init__(self):
		pass
	def worker(self,serverIP,serverPort):
		sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		sock.bind((serverIP, serverPort))
		while 1:
			data, addr = sock.recvfrom(512)
			Q = Query(data)
			sock.sendto(Q.response(), addr)
	def start(self,serverIP,serverPort):
		threading.Thread(target=self.worker, args=(serverIP,serverPort)).start()

class Query:
    def __init__(self,Q):
        self.header = Q[:12]
        self.question = Q[12:]
        #Extract out the ID of the message
        self.ID = self.header[:2]
        #Extract the FLAGS for parsing using parseflags()
        self.FLAGS = self.header[2:4]
        self.QR, self.Opcode, self.AA, self.TC, self.RD, self.RA, self.Z, self.RCODE = self.parseflags(self.FLAGS)
        #Parse additional header values
        self.QDCOUNT = ord(bytes(self.header[4:5]))*256 + ord(bytes(self.header[5:6]))
        self.ANCOUNT = ord(bytes(self.header[6:7]))*256 + ord(bytes(self.header[7:8]))
        self.NSCOUNT = ord(bytes(self.header[8:9]))*256 + ord(bytes(self.header[9:10]))
        self.ARCOUNT = ord(bytes(self.header[10:11]))*256 + ord(bytes(self.header[11:12]))
        #Begin parsing the question
        state = 0
        expectedlength = 0
        domainstring = ''
        self.QNAME = []
        x = 0
        y = 0
        for byte in self.question:
            if state == 1:
                if byte != 0:
                    domainstring += chr(byte)
                x += 1
                if x == expectedlength:
                    self.QNAME.append(domainstring)
                    domainstring = ''
                    state = 0
                    x = 0
                if byte == 0:
                    break
            else:
                state = 1
                expectedlength = byte
            y += 1
        #Extract the type and class
        self.QTYPE = self.question[y:y+2]
        self.QCLASS = self.question[y+2:y+4]

    def parseflags(self,FLAGS):
        self.QR = (ord(bytes(FLAGS[:1]))&128)>>7
        self.Opcode = (ord(bytes(FLAGS[:1]))&120)>>3
        self.AA = (ord(bytes(FLAGS[:1]))&4)>>2
        self.TC = (ord(bytes(FLAGS[:1]))&2)>>1
        self.RD = (ord(bytes(FLAGS[:1]))&1)
        self.RA = (ord(bytes(FLAGS[1:]))&128)>>7
        self.Z = (ord(bytes(FLAGS[1:]))&112)>>4
        self.RCODE = (ord(bytes(FLAGS[1:]))&15)
        return self.QR, self.Opcode, self.AA, self.TC, self.RD, self.RA, self.Z, self.RCODE

    def compileflags(self):
        Flags1 = (self.QR<<7 | self.Opcode<<3 | self.AA<<2 | self.TC<<1 | self.RD)
        Flags2 = (self.RA<<7 | self.Z<<4 | self.RCODE)
        return Flags1.to_bytes(1, byteorder='big') + Flags2.to_bytes(1, byteorder='big')

    def response(self):
        #set the flag for a response
        self.QR=1
        #set the flag for an NXDOMAIN and an empty answer - testing
        self.RCODE=3
        self.answer = bytearray()

        #compile the header and return the header, question and answer
        self.header = self.ID + self.compileflags() +self.QDCOUNT.to_bytes(2, byteorder='big')+self.ANCOUNT.to_bytes(2, byteorder='big')+self.NSCOUNT.to_bytes(2, byteorder='big')+self.ARCOUNT.to_bytes(2, byteorder='big')
        return self.header + self.question + self.answer
