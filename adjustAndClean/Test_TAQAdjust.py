import unittest
import numpy as np
from adjustAndClean.TAQAdjust import TAQAdjust

class Test_TAQAdjust2(unittest.TestCase):
    '''
    Class testing the correction of adjustment operations on prices and volumes.
    On the sample data given, both price and volume multipliers were 1.0.
    So for the sake of example we modified them to .5 and .25 respectively.
    Setters have been introduced in TAQAdjust only for that purpose.
    '''

    def test1(self):

        s_p500 = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/s_p500.xlsx'
        stackedTrades = np.array([['20070620', 'IBM', 34241000, 106.5, 85200.0], ['20070621', 'IBM', 57596000, 106.61000061035156, 500.0], ['20070621', 'IBM', 57596000, 106.61000061035156, 200.0], ['20070621', 'IBM', 57597000, 106.5999984741211, 200.0]])
        stackedQuotes = np.array([['20070620', 'IBM', 34241000, 106.5, 85200.0, 106.1, 8200.0], ['20070621', 'IBM', 57597000, 106.5, 85200.0, 106.1, 800.0]])
        
        adjuster = TAQAdjust( stackedQuotes, stackedTrades, s_p500 )
        
        # Initial quote check
        self.assertAlmostEquals( float(stackedQuotes[:,-4][0]), 106.5, 2 )
        self.assertAlmostEquals( float(stackedQuotes[:,-3][0]), 85200.0, 2 )
        self.assertAlmostEquals( float(stackedQuotes[:,-2][0]), 106.1, 2 )
        self.assertAlmostEquals( float(stackedQuotes[:,-1][0]), 8200.0, 2 )

        # Initial trade check
        self.assertAlmostEquals( float(stackedTrades[:,-2][0]), 106.5, 2 )
        self.assertAlmostEquals( float(stackedTrades[:,-1][0]), 85200.0, 2 )
        
        # On the sample data given, both price and volume multipliers were 1.0.
        # So for the sake of example we modified them.
        adjuster.getPriceMult("20070620")
        adjuster.getVolMult("20070620")
        adjuster.setPriceMult("20070620", 0.5)
        adjuster.setVolMult("20070620", 0.25)
        adjuster.getPriceMult("20070620")
        adjuster.getVolMult("20070620")
        
        # Adjust
        adjuster.adjustQuote()
        adjuster.adjustTrade()
        
        # Quote modification check
        self.assertAlmostEquals( float(stackedQuotes[:,-4][0]), 53.25, 2 )
        self.assertAlmostEquals( float(stackedQuotes[:,-3][0]), 21300.0, 2 )
        self.assertAlmostEquals( float(stackedQuotes[:,-2][0]), 53.05, 2 )
        self.assertAlmostEquals( float(stackedQuotes[:,-1][0]), 2050.0, 2 )

        # Trade modification check
        self.assertAlmostEquals( float(stackedTrades[:,-2][0]), 53.25, 2 )
        self.assertAlmostEquals( float(stackedTrades[:,-1][0]), 21300.0, 2 )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()