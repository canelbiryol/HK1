'''
Created on Mar 8, 2018

@author: canelbiryol
'''
import unittest
import numpy as np
from partB.xMinuteReturn import getXSecMidQuoteReturns, getXSecTradeReturns

class Test(unittest.TestCase):


    def test1(self):
        stackedTrades = np.array([['20070620', 'IBM', 34241000, 106.5, 85200.0], ['20070621', 'IBM', 34242000, 106.5, 500.0], 
                                  ['20070621', 'IBM', 34243000, 106.5, 200.0], ['20070621', 'IBM', 34244000, 106.5, 200.0]])
        stackedQuotes = np.array([['20070620', 'IBM', 34241000, 106.5, 85200.0, 106.1, 8200.0], ['20070621', 'IBM', 34241000, 106.5, 85200.0, 106.1, 800.0]])
        
        tradereturns = getXSecTradeReturns(stackedTrades, 1)
        quotereturns = getXSecMidQuoteReturns(stackedQuotes, 1)
       
        self.assertTrue( tradereturns[0] == [0.0, 0.0, 0.0] )
        self.assertTrue( quotereturns[0] == [0.0] )
       
        # converted date + timestamps to epoch
        # https://www.epochconverter.com/
        self.assertTrue( tradereturns[1] == [1182346242.0, 1182346243.0, 1182346244.0] )
        self.assertTrue( quotereturns[1] == [1182346242.0] )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()