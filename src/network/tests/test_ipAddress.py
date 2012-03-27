'''
Created on Jun 14, 2011

@author: lebleu1
'''
import unittest
from network.ipAddress import IpAddress

class Test(unittest.TestCase):
    
    
    def testPack(self):
        address = IpAddress("192.168.1.12")
        self.assertEquals("\xC0\xA8\x01\x0C",address.pack())
