import struct

class Eth2Header(object):
    def __init__(self):
        self.DestinationMac = "00:00:00:00:00:00"   # string for 48 bits
        self.SourceMac = "00:00:00:00:00:00"        # string for 48 bits
        self.Type = 0x0800                          # 16 bits
    
    def compute_crc32byte(self,crc_val,val):
        GEN = 0x04C11DB7                            # This value from: G(x) = x32+x26+x23+x22+x16+x12+x11+x10+x8+x7+x5+x4+x2+x+1
        shift_reg = crc_val ^ (val << 24)           # XOR all new bits at once
        for i in [0,1,2,3,4,5,6,7]:
            leading_bit = shift_reg & 0x80000000    # save leading bit
            shift_reg = shift_reg << 1              # shift 1 bit left
            if(leading_bit):
                shift_reg = shift_reg ^ GEN
        return shift_reg
    
    def reverseByteBits(self, input):
        rtn = ((input>>7) & 0x01)
        rtn |= (((input>>6) & 0x01) << 1)
        rtn |= (((input>>5) & 0x01) << 2)
        rtn |= (((input>>4) & 0x01) << 3)
        rtn |= (((input>>3) & 0x01) << 4)
        rtn |= (((input>>2) & 0x01) << 5)
        rtn |= (((input>>1) & 0x01) << 6)
        rtn |= (((input) & 0x01) << 7)
        return rtn & 0xFF
    
    def compute_checksum(self, anArray):
        crc = 0xFFFFFFFF                                                                # initial value : this complement the first 32 bits of message
        for i in range(len(anArray)):                                                   # for each byte in the array...
            crc = self.compute_crc32byte(crc, self.reverseByteBits(ord(anArray[i])))    # compute the crc32 of the byte
        crc = (crc ^ 0xFFFFFFFF)                                                        # complement of remainder of the crc
        ''' Flip Bytes in place. '''
        crc = ((self.reverseByteBits((crc>>24))<<24) | (crc & 0x00FFFFFF))              # Flip bits of first byte  : abcd -> dcba
        crc = ((self.reverseByteBits((crc>>16))<<16) | (crc & 0xFF00FFFF))              # Flip bits of second byte : abcd -> dcba
        crc = ((self.reverseByteBits((crc>>8))<<8)   | (crc & 0xFFFF00FF))              # Flip bits of third byte  : abcd -> dcba
        crc = (self.reverseByteBits(crc)             | (crc & 0xFFFFFF00))              # Flip bits of fourth byte : abcd -> dcba
        return (crc) & 0xFFFFFFFF                                                       # return 32 bit truncated checksum

    def createHeader(self,payload):
        D1,D2,D3,D4,D5,D6 = (self.DestinationMac).split(':')
        D1 = int(D1,16)
        D2 = int(D2,16)
        D3 = int(D3,16)
        D4 = int(D4,16)
        D5 = int(D5,16)
        D6 = int(D6,16)
        
        S1,S2,S3,S4,S5,S6 = (self.SourceMac).split(':')
        S1 = int(S1,16)
        S2 = int(S2,16)
        S3 = int(S3,16)
        S4 = int(S4,16)
        S5 = int(S5,16)
        S6 = int(S6,16)
        
        formatString = "!6B6BH%dsI"%len(payload)
        checkSum = self.compute_checksum(struct.pack(formatString[:-1], D1,D2,D3,D4,D5,D6, S1,S2,S3,S4,S5,S6, self.Type, payload))
        return struct.pack(formatString, D1,D2,D3,D4,D5,D6, S1,S2,S3,S4,S5,S6, self.Type, payload, checkSum)

if __name__ == "__main__":
    eth = Eth2Header()
    print eth.compute_checksum([])
    print eth.createHeader("test payload")
