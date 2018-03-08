import unittest
import numpy as np
from adjustAndClean.TAQCleaner import TAQCleaner

class Test_TAQCleaner(unittest.TestCase):
    '''
    Testing cleaning on a simple example
    '''
    
    def test1(self):
        stackedTrades = np.array([['20070620', 'IBM', 34241000, 106.5, 85200.0], ['20070621', 'IBM', 57596000, 106.61000061035156, 500.0], ['20070621', 'IBM', 57596000, 106.61000061035156, 200.0], ['20070621', 'IBM', 57597000, 106.5999984741211, 200.0], ['20070621', 'IBM', 57597000, 106.5999984741211, 200.0], ['20070621', 'IBM', 57597000, 106.5999984741211, 200.0]])
        stackedQuotes = np.array([['20070620', 'IBM', 34241000, 106.5, 85200.0, 106.1, 8200.0], ['20070621', 'IBM', 57597000, 106.5, 85200.0, 106.1, 800.0], ['20070621', 'IBM', 57597000, 106.5, 85200.0, 106.1, 800.0], ['20070621', 'IBM', 57597000, 106.5, 85200.0, 106.1, 800.0], ['20070621', 'IBM', 57597000, 106.5, 85200.0, 106.1, 800.0]])

        cleaner = TAQCleaner(stackedQuotes, stackedTrades)
        
        # Initial quote check
        self.assertAlmostEquals( float(stackedQuotes[:,-4][0]), 106.5, 2 )
        self.assertAlmostEquals( float(stackedQuotes[:,-2][0]), 106.1, 2 )

        # Initial trade check
        self.assertAlmostEquals( float(stackedTrades[:,-2][0]), 106.5, 2 )
        
        
        # Perturbation of the first midprice by a factor 10000
        stackedQuotes[:,-4][0] = float(stackedQuotes[:,-4][0]) * 10000
        stackedQuotes[:,-2][0] = float(stackedQuotes[:,-2][0]) * 10000
        
        # Perturbation of the first trade price by a factor 10000
        stackedTrades[:,-2][0] = float(stackedTrades[:,-2][0]) * 10000

        # Check the execution of the perturbations
        self.assertAlmostEquals( float(stackedQuotes[:,-4][0]), 1065000.0, 2 )
        self.assertAlmostEquals( float(stackedQuotes[:,-2][0]), 1061000.0, 2 )
        self.assertAlmostEquals( float(stackedTrades[:,-2][0]), 1065000.0, 2 )
        
        # Execute quote cleaning
        stackedQuotes = np.delete(stackedQuotes, cleaner.cleanQuotesIndices(), axis = 0)
        
        # Execute trade cleaning
        stackedTrades = np.delete(stackedTrades, cleaner.cleanTradesIndices(), axis = 0)
        
        # Display
        print(stackedQuotes)
        print(stackedTrades)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()