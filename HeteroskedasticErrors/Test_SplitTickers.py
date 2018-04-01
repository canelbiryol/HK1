import unittest
from HeteroskedasticErrors.SplitTickers import SplitTickers

class Test_SplitTickers(unittest.TestCase):
    '''
    Class allowing to visually test the outputs of the SplitTicjers class.
    '''
    
    def test1(self):

        s = SplitTickers()
        
        # Display
        print(s.getActiveStocks())
        print(s.getPassiveStocks())
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()