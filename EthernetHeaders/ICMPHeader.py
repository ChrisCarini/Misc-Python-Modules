import struct
        
class ICMPHeader(object):
    def __init__(self, type=8):
        self.Type     = type # 8 = Echo request ; 0 = Echo reply
        self.Code     = 0
        self.CheckSum = 0
        self.ID       = 0
        self.Seq      = 1
        self.Data     = "!abcdef0123456789!"
    
    def __carry_around_add(self, a, b):
        c = a + b
        return (c & 0xffff) + (c >> 16)

    def __calcCheckSum(self,msg): # http://stackoverflow.com/questions/1767910/checksum-udp-calculation-python
        s = 0
        for i in range(0, len(msg), 2):
            if( i+1 != len(msg) ):
                w = (ord(msg[i]) << 8) + (ord(msg[i+1]))
            else:
                w = (ord(msg[i]) << 8)
            s = self.__carry_around_add(s, w)
        return ~s & 0xffff
        
    def createHeader(self,data,id=-1,seq=-1):
        if(id == -1):
            self.ID += 1
            self.ID %= 65535
        else:
            self.ID = id
        if(seq == -1):
            pass
        else:
            self.Seq = seq
        self.Data = data
        
        firstWord  = self.Type << 24
        firstWord |= self.Code << 16

        secondWord  = self.ID << 16
        secondWord |= self.Seq
        
        tmpMessage = struct.pack("!II", (firstWord|0x0000), secondWord) + self.Data
        self.CheckSum = self.__calcCheckSum(tmpMessage)
        firstWord |= self.CheckSum

        self.Seq += 1

        return struct.pack("!II", firstWord, secondWord) + self.Data, 8 + len(self.Data)

if __name__ == "__main__":
    icmp = ICMPHeader()
    print icmp.__calcCheckSum()
    print icmp.createHeader("test data")
