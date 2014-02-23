import Eth2Header
import IPHeader
import ICMPHeader
import UDPHeader

if __name__ == "__main__":
    eth = Eth2Header.Eth2Header()
    print "Eth2Header Checksum: %s" % eth.compute_checksum([])
    print "Eth2Header Header: %s" % eth.createHeader("test payload")
    
    ip = IPHeader.IPHeader(0x11)
    print "IPHeader Header: %s" % ip.createHeader(srcIP="1.2.3.4",destIP="5.6.7.8",dataLen=10)
    
    icmp = ICMPHeader.ICMPHeader()
    tmp = icmp.createHeader("test data")
    print "ICMPHeader Header: %s" % tmp[0]
    print "ICMPHeader Header Length: %s" % tmp[1]

    udp = UDPHeader.UDPHeader()
    tmp = udp.createHeader(srcPort = 80, dstPort = 80, data="GET")
    print "UDPHeader Header: %s" % tmp[0]
    print "UDPHeader Header Length: %s" % tmp[1]

    print "##########################"
    print "#  Make some test stuff  #"
    print "##########################"
    def makePacket(SRC_IP,SRC_UDP,DST_IP,DST_UDP,data,seqNum=0):
        EthHeaderObj             = Eth2Header.Eth2Header()  # Retrieve header from .createHeader()
        IPHeaderObj              = IPHeader.IPHeader(0x11)  # Retrieve header from .createHeader(<srcIP>, <destIP>, <dataLen>)
        if( (SRC_UDP == 0) and (DST_UDP == 0) ):
            IPICMPHeaderObj      = IPHeader.IPHeader(0x01)  # Retrieve header from .createHeader(<srcIP>, <destIP>, <dataLen>)
            ICMPHeaderObj        = ICMPHeader.ICMPHeader()  # Retrieve header from .createHeader()
        else:
            UDPHeaderObj         = UDPHeader.UDPHeader()    # Retrieve header from .createHeader(<srcPort>, <dstPort>, <data>)

    
        packet = ""                                                                             # Initalize the packet to be empty
        dataToSend = data+"|%d" % ( seqNum )                                                    # Assemble the data to be sent
        if( DST_UDP == 0 ):                                                                     # If destination port is zero, must be ICMP...
            icmpHeader, icmpLen = ICMPHeaderObj.createHeader(dataToSend)                        # Create ICMP header
            ipICMPHeader        = IPICMPHeaderObj.createHeader(SRC_IP, DST_IP, icmpLen)         # Create IP ICMP header
            packet              = EthHeaderObj.createHeader(ipICMPHeader + icmpHeader)          # Append all headers and data together
        else:                                                                                   # Otherwise, destination port is non-zero, must be UDP...
            udpHeader, udpLen   = UDPHeaderObj.createHeader(SRC_UDP, DST_UDP, dataToSend)       # Create UDP header
            ipHeader            = IPHeaderObj.createHeader(SRC_IP, DST_IP, udpLen)              # Create IP header
            packet              = EthHeaderObj.createHeader(ipHeader + udpHeader + dataToSend)  # Append all headers and data together
        seqNum += 1                                                                             # Increment sequence number
        return packet                                                                           # Return packet
    
    print "Packet Info:\n\tSrc IP:\t\t%s\n\tSrc Port:\t%s\n\tDst IP:\t\t%s\n\tDst Port:\t%s\n\tData:\t\t%s\n"%("1.2.3.4",80,"5.6.7.8",80,"test data")
    pkt = makePacket("1.2.3.4",80,"5.6.7.8",80,"test data")
    print "Packet: %s"%(pkt)