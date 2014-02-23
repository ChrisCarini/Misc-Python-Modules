import struct

class IPHeader(object):
    def __init__(self, protocol):
        self.Version        = 4        # 4 bits
        self.IHL            = 5        # 4 bits    (5 32 bit words in the header)
        self.DSCP           = 0        # 6 bits
        self.ECN            = 0        # 2 bits
        self.TotalLen       = 0        # 16 bits

        self.ID             = 0        # 16 bits
        self.Flags          = 0        # 3 bits
        self.FragOff        = 0        # 13 bits

        self.TTL            = 128      # 8 bits
        self.Protocol       = protocol # 8 bits (UDP=0x11, ICMP=0x01)
        self.HeaderCheckSum = 0        # 16 bits

        self.SourceIP       = 0
        self.DestIP         = 0
        
    def __ipStrToInt(self, ipStr):
        a, b, c, d = ipStr.split('.')
        return( int(a) <<24 | int(b) <<16 | int(c) <<8 | int(d) )

    def __carry_around_add(self, a, b):
        c = a + b
        return (c & 0xffff) + (c >> 16)

    def __calcCheckSum(self):
        rtnSum = 0
        tempSum = (self.Version << 12) | (self.IHL << 8) | (self.DSCP << 2) | (self.ECN)
        rtnSum = self.__carry_around_add(rtnSum, tempSum)
        tempSum = self.TotalLen
        rtnSum = self.__carry_around_add(rtnSum, tempSum)
        tempSum = self.ID
        rtnSum = self.__carry_around_add(rtnSum, tempSum)
        tempSum = (self.Flags << 13) | self.FragOff
        rtnSum = self.__carry_around_add(rtnSum, tempSum)
        tempSum = (self.TTL << 8) | self.Protocol
        rtnSum = self.__carry_around_add(rtnSum, tempSum)
        tempSum = (self.SourceIP >> 16)
        rtnSum = self.__carry_around_add(rtnSum, tempSum)
        tempSum = (self.SourceIP & 0xFFFF)
        rtnSum = self.__carry_around_add(rtnSum, tempSum)
        tempSum = (self.DestIP >> 16)
        rtnSum = self.__carry_around_add(rtnSum, tempSum)
        tempSum = (self.DestIP & 0xFFFF)
        rtnSum = self.__carry_around_add(rtnSum, tempSum)
    
        return ~rtnSum & 0xffff

    def createHeader(self, srcIP, destIP, dataLen):
        self.ID            += 1
        self.ID            %= 65535
        self.TotalLen       = 20 + dataLen
        self.SourceIP       = self.__ipStrToInt(srcIP)
        self.DestIP         = self.__ipStrToInt(destIP)
        self.HeaderCheckSum = self.__calcCheckSum()

        firstWord  = self.Version << 28
        firstWord |= self.IHL << 24
        firstWord |= self.DSCP << 18
        firstWord |= self.ECN << 16
        firstWord |= self.TotalLen
        firstWord &= 0xFFFFFFFF
        
        secondWord  = self.ID << 16
        secondWord |= self.Flags << 13
        secondWord |= self.FragOff
        secondWord &= 0xFFFFFFFF

        thirdWord  = self.TTL << 24
        thirdWord |= self.Protocol << 16
        thirdWord |= self.HeaderCheckSum
        thirdWord &= 0xFFFFFFFF

        return struct.pack("!IIIII", firstWord, secondWord, thirdWord, self.SourceIP, self.DestIP)        

if __name__ == "__main__":
    ip = IPHeader(0x11)
    print ip.__calcCheckSum()
    print ip.compute_checksum([])
