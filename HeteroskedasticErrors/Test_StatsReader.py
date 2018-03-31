import unittest
import numpy as np
from HeteroskedasticErrors.StatsReader import StatsReader

class Test_StatsReader(unittest.TestCase):
    '''
    Class allowing to visually test the outputs of the StatsReader class.
    '''
    
    def test1(self):
        stats = StatsReader('/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/stats/stats.xlsx')
        
        # Display
        print(stats.get2minRetArraysVector())
              
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()