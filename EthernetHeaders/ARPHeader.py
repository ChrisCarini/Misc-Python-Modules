import struct
        
class ARPHeader(object):
    def __init__(self, sAddrIP, sAddrMAC, tAddrIP, tAddrMAC="00:00:00:00:00:00", oper=1):
        self.HTYPE      = 0x01      # 2 bytes; Hardware Type (Ethernet = 1)
        self.PTYPE      = 0x0800    # 2 bytes; Protocol Type (IPv4 = 0x0800)
        self.HLEN       = 0x06      # 1 byte ; Hardware Address Length (Length in octets of HW Addr, Ethernet = 6)
        self.PLEN       = 0x04      # 1 byte ; Protocol Address Length (Length in octets of Addr in upper layer proto (proto in PTYPE), IPv4 = 4)
        self.OPER       = oper      # 2 bytes; Operation (Operation of packet, Request = 1, Reply = 2)
        self.SHA        = sAddrMAC  # 6 bytes; Sender Hardware Address (Media address of sender)
        self.SPA        = sAddrIP   # 4 bytes; Sender Protocol Address (Internetwork address of sender)
        self.THA        = tAddrMAC  # 6 bytes; Target Hardware Address (Media address of intended receiver; ignored in requests)
        self.TPA        = tAddrIP   # 4 bytes; Target Protocol Address (Internetwork address of intended receiver)
    
    def __ipStrToInt(self, ipStr):
        a, b, c, d = ipStr.split('.')
        return( int(a) <<24 | int(b) <<16 | int(c) <<8 | int(d) )
    
    def createHeader(self):
        formatString = "!HHBBH6BI6BI"
        
        S1,S2,S3,S4,S5,S6 = (self.SHA).split(':')
        S1 = int(S1,16)
        S2 = int(S2,16)
        S3 = int(S3,16)
        S4 = int(S4,16)
        S5 = int(S5,16)
        S6 = int(S6,16)
        D1,D2,D3,D4,D5,D6 = (self.THA).split(':')
        D1 = int(D1,16)
        D2 = int(D2,16)
        D3 = int(D3,16)
        D4 = int(D4,16)
        D5 = int(D5,16)
        D6 = int(D6,16)
        
        return struct.pack(formatString, self.HTYPE, self.PTYPE, self.HLEN, self.PLEN, self.OPER, S1,S2,S3,S4,S5,S6, self.__ipStrToInt(self.SPA), D1,D2,D3,D4,D5,D6, self.__ipStrToInt(self.TPA) )

if __name__ == "__main__":
    arp = ARPHeader()
    
    ###        ###
    #    Demo    #
    ###        ###
    # Create ARP request header for the following:
    #       SRC: 192.168.1.1  - BE:EF:BE:EF:BE:EF
    #       DST: 192.168.1.20 - ?? Unknown ??
    #   Response of:
    #       ?? Unknown ?? -> "F0:0D:F0:0D:F0:0D"
    
    # create ARP request header
    print arp.createHeader("192.168.1.1", "BE:EF:BE:EF:BE:EF", "192.168.1.20", oper=1)
    
    # create ARP response header
    print arp.createHeader("192.168.1.20", "F0:0D:F0:0D:F0:0D", tAddrMAC="F0:0D:DE:AD:BE:EF", "192.168.1.1", oper=2)
