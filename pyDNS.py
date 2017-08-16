'''
Header
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

Question
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

DNS RR response
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

                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                                               |
    /                                               /
    /                      NAME                     /
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TYPE                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                     CLASS                     |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      TTL                      |
    |                                               |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                   RDLENGTH                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--|
    /                     RDATA                     /
    /                                               /
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
'''


class Query:
    def __init__(self,Q):
        self.header = Q[:12]
        self.question = Q[12:]
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
        self.QTYPE = self.question[y:y+2]
        self.QCLASS = self.question[y+2:y+4]
        self.ID = self.header[:2]
        self.FLAGS = self.header[2:4]
        self.QR, self.Opcode, self.AA, self.TC, self.RD, self.RA, self.Z, self.RCODE = self.parseflags(self.FLAGS)
        self.QDCOUNT = ord(bytes(self.header[4:5]))*256 + ord(bytes(self.header[5:6]))
        self.ANCOUNT = ord(bytes(self.header[6:7]))*256 + ord(bytes(self.header[7:8]))
        self.NSCOUNT = ord(bytes(self.header[8:9]))*256 + ord(bytes(self.header[9:10]))
        self.ARCOUNT = ord(bytes(self.header[10:11]))*256 + ord(bytes(self.header[11:12]))

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



    def response(self):
        #set the flag for a response
        self.QR=1
        #set the flag for an NXDOMAIN - for testing
        self.RCODE=3

        Flags1 = (self.QR<<7 | self.Opcode<<3 | self.AA<<2 | self.TC<<1 | self.RD)
        Flags2 = (self.RA<<7 | self.Z<<4 | self.RCODE)
        self.header = self.ID + Flags1.to_bytes(1, byteorder='big') + Flags2.to_bytes(1, byteorder='big')+self.QDCOUNT.to_bytes(2, byteorder='big')+self.ANCOUNT.to_bytes(2, byteorder='big')+self.NSCOUNT.to_bytes(2, byteorder='big')+self.ARCOUNT.to_bytes(2, byteorder='big')
        return self.header + self.question
