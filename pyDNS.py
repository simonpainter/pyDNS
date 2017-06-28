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
	return {'ID':ID, 'QR':QR, 'Opcode':Opcode, 'AA':AA, 'TC':TC, 'RD':RD, 'RA':RA, 'Z':Z, 'RCODE':RCODE,'QDCOUNT':QDCOUNT,'ANCOUNT':ANCOUNT,'NSCOUNT':NSCOUNT,'ARCOUNT':ARCOUNT}

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
    state = 0
    expectedlength = 0
    domainstring = ''
    QNAME = []
    x = 0
    y = 0
    for byte in question:
        if state == 1:
            if byte != 0:
                domainstring += chr(byte)
            x += 1
            if x == expectedlength:
                QNAME.append(domainstring)
                domainstring = ''
                state = 0
                x = 0
            if byte == 0:
                break
        else:
            state = 1
            expectedlength = byte
        y += 1

    QTYPE = question[y:y+2]
    QCLASS = question[y+2:y+4]
    return {'QNAME':QNAME,'QTYPE':QTYPE,'QCLASS':QCLASS}


#DNS RR response
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
def buildresponse(Q):
    #set the flag for a response
    Q['QR']=1
    #set the flag for an NXDOMAIN - for testing
    Q['RCODE']=3
    TransactionID = (Q['ID'])
    Flags1 = (Q['QR']<<7 | Q['Opcode']<<3 | Q['AA']<<2 | Q['TC']<<1 | Q['RD'])
    Flags2 = (Q['RA']<<7 | Q['Z']<<4 | Q['RCODE'])
    header = TransactionID + Flags1.to_bytes(1, byteorder='big') + Flags2.to_bytes(1, byteorder='big')+Q['QDCOUNT'].to_bytes(2, byteorder='big')+Q['ANCOUNT'].to_bytes(2, byteorder='big')+Q['NSCOUNT'].to_bytes(2, byteorder='big')+Q['ARCOUNT'].to_bytes(2, byteorder='big')
    print(header)
    return header
