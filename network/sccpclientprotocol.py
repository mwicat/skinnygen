'''
Created on Jun 14, 2011

@author: lebleu1
'''
from twisted.protocols.basic import IntNStringReceiver
import struct
from sccp.messagefactory import MessageFactory

class SCCPClientProtocol(IntNStringReceiver):
    """ The protocol is based on twisted.protocols.basic
        IntNStringReceiver, with little-endian 32-bit 
        length prefix.
    """
    structFormat = "<L"
    prefixLength = struct.calcsize(structFormat)
    trailingNbOfBytes = 4
    messageFactory = MessageFactory()
    
    def dataReceived(self, recd):
        """
        Convert int prefixed strings into calls to stringReceived.
        """
        self.recvd = self.recvd + recd
        while len(self.recvd) >= self.prefixLength and not self.paused:
            length ,= struct.unpack(
                self.structFormat, self.recvd[:self.prefixLength])
            length=length+self.trailingNbOfBytes
            
            if length > self.MAX_LENGTH:
                self.lengthLimitExceeded(length)
                return
            if len(self.recvd) < length + self.prefixLength:
                break
            packet = self.recvd[self.prefixLength:length + self.prefixLength]
            self.recvd = self.recvd[length + self.prefixLength:]
            self.stringReceived(packet)

    def stringReceived(self, s):    
        message = self.messageFactory.create(s)
        message.unPack(s[8:])
        self.factory.handleMessage(message)


    def connectionMade(self):
        self.transport.setTcpNoDelay(True)
        self.factory.clientReady(self)
    
        
    def sendString(self, data):
        self.transport.write(struct.pack(self.structFormat, len(data)) + data+"\x00\x00\x00\x00")
