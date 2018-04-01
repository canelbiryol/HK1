import unittest
from HeteroskedasticErrors.SplitTickers import SplitTickers

class Test_SplitTickers(unittest.TestCase):
    '''
    Class allowing to visually test the outputs of the StatsReader class.
    '''
    
    def test1(self):
        #stats = SplitTickers('/media/louis/DATA/cleandata/trades')
        # Display
        
        #TODO: end!
        print('/media/louis/DATA/cleandata/trades/20070801/AAPL_trades.binRT')
        #print(stats, "done")              
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()