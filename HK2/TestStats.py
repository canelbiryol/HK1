'''
Created on Apr 3, 2018

@author: canelbiryol
'''
import unittest
from HK2.Stats import Stats

times = {
    '9:30': 19 * 60 * 60 * 1000 / 2,
    '15:30': 31 * 60 * 60 * 1000 / 2,
    '16:00': 16 * 60 * 60 * 1000,
    '2min': 2 * 60 * 100
}

class Test_Stats(unittest.TestCase):


    def test1(self):
        trades = [['20070620', 34334000, 54.30149841308594, 38800.0],
                 ['20070620', 34335000, 54.30149841308594, 100.0],
                 ['20070620', 34335000, 54.30149841308594, 100.0],
                 ['20070620', 34335000, 54.30149841308594, 100.0],
                 ['20070620', 34336000, 54.30149841308594, 100.0]]
        
        quotes = [['20070620', 34334000, 54.1495475769043, 3.0, 54.34293746948242, 10.0],
                 ['20070620', 34334000, 54.1495475769043, 3.0, 54.34293746948242, 12.0],
                 ['20070620', 34334000, 54.1495475769043, 3.0, 54.32912826538086, 1.0],
                 ['20070620', 34335000, 54.163360595703125, 1.0, 54.32912826538086, 1.0],
                 ['20070620', 34335000, 54.163360595703125, 1.0, 54.34293746948242, 12.0]]
        
        statsClass = Stats(trades, quotes)
        
        arrival_price = statsClass.getArrivalPrice(5)
        self.assertAlmostEqual( arrival_price, 54.24, 1 )
        terminal_price = statsClass.getTerminalPrice(5)
        self.assertAlmostEqual( terminal_price, 54.24, 1 )
        imbalance = statsClass.getImbalance(times['9:30'], times['15:30']) 
        self.assertAlmostEqual( imbalance, 0, 1 )      
        VWAPuntil330 = statsClass.getVWAP(times['9:30'], times['15:30'])
        self.assertAlmostEqual( VWAPuntil330, 54.30, 1 )
        VWAPuntil400 = statsClass.getVWAP(times['9:30'], times['16:00'])   
        self.assertAlmostEqual( VWAPuntil400, 54.30, 1 ) 
        vol = statsClass.getTotalDailyVol()
        self.assertAlmostEqual( vol, 171675000 )



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()