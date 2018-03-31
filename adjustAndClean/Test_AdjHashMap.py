import unittest
from adjustAndClean.AdjustingHashmap import AdjustingHashmap

class Test_AdjHashMap(unittest.TestCase):
    '''
    This class tests the functionality of the methods addQuotes and addTrades of the class StackData.
    It works on the base directory provided by the user, and apply them to the IBM ticker.
    '''

    def test1(self):
        s_p500 = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/s_p500.xlsx'
        
        multmap = AdjustingHashmap(s_p500)
        
        self.assertAlmostEquals( multmap.getPriceMultiplier('MWV', '20070920'), 0.976767, 2 )
        self.assertAlmostEquals( multmap.getVolMultiplier('MWV', '20070920'), 0.78, 2 )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()