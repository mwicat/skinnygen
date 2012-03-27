'''
Created on Jun 14, 2011

@author: lebleu1
'''
import unittest
from sccp.sccpregister import SCCPRegister
from struct import pack
from sccp.sccpmessagetype import SCCPMessageType


class Test(unittest.TestCase):

    sccpRegister = SCCPRegister("SEP00164697AAAA", "192.168.1.2")


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testPack(self):
        
        registerPack = pack('I',0)
        registerPack = registerPack + pack('I',SCCPMessageType.RegisterMessage)
        registerPack = registerPack + "SEP00164697AAAA"+"\x00"
        registerPack = registerPack + pack('II',0,1)
        registerPack = registerPack + pack('BBBB',192,168,1,2)
        registerPack = registerPack + pack('III',8,0,0)
        registerPack = registerPack + '\x0B'+ '\x00'+ '\x60'+ '\x85'
        registerPack = registerPack + pack('IIII',0,0,0,0)

        self.assertEquals(registerPack,self.sccpRegister.pack())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()