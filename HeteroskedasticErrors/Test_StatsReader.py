import unittest
from HeteroskedasticErrors.StatsReader import StatsReader

class Test_StatsReader(unittest.TestCase):
    '''
    Class allowing to visually test the outputs of the StatsReader class.
    '''
    
    def test1(self):
        stats = StatsReader('/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/stats/stats.xlsx', boolDisplay=False)
        
        print(stats.getADVolVector())
        print(stats.getADValuesVector())
        print(stats.getStdErrorVector())
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()