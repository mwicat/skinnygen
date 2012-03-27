'''
Created on Jun 14, 2011

@author: lebleu1
'''
import unittest
from sccp.sccpdefinetimedate import SCCPDefineTimeDate


class TestSccpDefineDateTime(unittest.TestCase):


    def testUnPack(self):
        defineDateTime = SCCPDefineTimeDate()
        receivedBuffer = '\xdb\x07\x00\x00\x06\x00\x00\x00\x04\x00\x00\x00\x09\x00\x00\x00' \
            '\x12\x00\x00\x00\x2a\x00\x00\x00\x25\x00\x00\x00\x0F\x00\x00\x00\xfd\xf7\xf0\x4d'
        defineDateTime.unPack(receivedBuffer)
        self.assertEquals(defineDateTime.year,2011)
        self.assertEquals(defineDateTime.month,6)
        self.assertEquals(defineDateTime.dayOfWeek,4)
        self.assertEquals(defineDateTime.day,9)
        self.assertEquals(defineDateTime.hour,18)
        self.assertEquals(defineDateTime.minute,42)
        self.assertEquals(defineDateTime.seconds,37)
        self.assertEquals(defineDateTime.milliseconds,15)
        self.assertEquals(defineDateTime.timestamp,1307637757)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()