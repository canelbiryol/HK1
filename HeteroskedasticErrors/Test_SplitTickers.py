import unittest
from HeteroskedasticErrors.SplitTickers import SplitTickers

class Test_SplitTickers(unittest.TestCase):
    '''
    Class allowing to visually test the outputs of the SplitTicjers class.
    '''
    
    def test1(self):
        indicestoDrop = [9, 28, 60, 79, 100, 104, 114, 137, 196, 246, 271, 324, 378, 388, 398, 407, 413, 425, 432, 444, 458]

        s = SplitTickers(indicesToDrop=indicestoDrop)
        
        # Display
        print(s.getActiveStocks())
        print(s.getPassiveStocks())
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()