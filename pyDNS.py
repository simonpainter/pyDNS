#Parse the header
'''
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      ID                       |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    QDCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ANCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    NSCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ARCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
'''
def parseflags(FLAGS):
	QR = (ord(bytes(FLAGS[:1]))&128)>>7
	Opcode = (ord(bytes(FLAGS[:1]))&120)>>3
	AA = (ord(bytes(FLAGS[:1]))&4)>>2
	TC = (ord(bytes(FLAGS[:1]))&2)>>1
	RD = (ord(bytes(FLAGS[:1]))&1)
	RA = (ord(bytes(FLAGS[1:]))&128)>>7
	Z = (ord(bytes(FLAGS[1:]))&112)>>4
	RCODE = (ord(bytes(FLAGS[1:]))&15)
	return QR, Opcode, AA, TC, RD, RA, Z, RCODE
def parseheader(header):
	ID = header[:2]
	FLAGS = header[2:4]
	QR, Opcode, AA, TC, RD, RA, Z, RCODE = parseflags(FLAGS)
	QDCOUNT = ord(bytes(header[4:5]))*256 + ord(bytes(header[5:6]))
	ANCOUNT = ord(bytes(header[6:7]))*256 + ord(bytes(header[7:8]))
	NSCOUNT = ord(bytes(header[8:9]))*256 + ord(bytes(header[9:10]))
	ARCOUNT = ord(bytes(header[10:11]))*256 + ord(bytes(header[11:12]))
	return ID, QR, Opcode, AA, TC, RD, RA, Z, RCODE,QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT

#Parse the question
'''
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                     QNAME                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QTYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     QCLASS                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
'''
def parsequestion(question):
	QNAME=''
	QTYPE=''
	QCLASS=''
	return QNAME,QTYPE,QCLASS
