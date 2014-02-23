import struct

class UDPHeader(object):
    def __init__(self):
        self.SrcPort  = 0   # 16 bits
        self.DestPort = 0   # 16 bits
        self.Length   = 0   # 16 bits
        self.CheckSum = 0   # 16 bits, leaving 0 (not calculating)
        self.Data     = ""  #
        
    def __calcCheckSum(self):
        ## TODO: Template for a CheckSum Calculator
        return self.CheckSum
        
    def createHeader(self, srcPort, dstPort, data):
        self.SrcPort = srcPort
        self.DestPort = dstPort
        self.Data = data
        self.Length = 8 + len(self.Data)
        return struct.pack("!HHHH", self.SrcPort, self.DestPort, self.Length, self.__calcCheckSum()), self.Length

if __name__ == "__main__":
    udp = UDPHeader()
    print udp.__calcCheckSum()
    print udp.createHeader(srcPort = 80, dstPort = 80, data="GET")
