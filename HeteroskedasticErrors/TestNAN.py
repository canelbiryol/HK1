import unittest
import numpy as np
import pandas as pd

class Test_StatsReader(unittest.TestCase):
    '''
    Class allowing to visually test the outputs of the StatsReader class.
    '''
    
    def test1(self):
        df = pd.DataFrame([[0,1,3,4,np.nan,2],[3,5,6,np.nan,3,3]])
        
        print(np.where(np.asanyarray(np.isnan(df))))

        print(np.array(np.where(np.asanyarray(np.isnan(df))))[:,0])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()