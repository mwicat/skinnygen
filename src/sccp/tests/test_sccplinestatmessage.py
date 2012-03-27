'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp.sccplinestat import SCCPLineStat
import unittest


class TestLineStat(unittest.TestCase):


    def testUnPack(self):
        lineStat = SCCPLineStat()
        receivedBuffer = '\x04\x00\x00\x00\x31\x30\x32\x31\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        lineStat.unPack(receivedBuffer)
        self.assertEquals(lineStat.line,4)
        self.assertEquals(lineStat.dirNumber,'1021')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()