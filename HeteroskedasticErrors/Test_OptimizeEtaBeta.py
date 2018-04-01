import unittest
import numpy as np
from HeteroskedasticErrors import OptimizeEtaBeta
from HeteroskedasticErrors.OptimizeEtaBeta import getOptimalEtaBeta

class Test_OptimizeEtaBeta(unittest.TestCase):

    def test1(self):
        '''
        Test to see if our OptimizeEtaBeta code works
        First let's create some fake data in a universe of 1000 days and 4 stocks.
        The stocks have similar behaviors and different StdErrs to account for heteroskedasticity.
        '''
        
        sigmas = np.zeros(4000)
        imbalances = np.zeros(4000)
        ADVs = np.zeros(4000)
        StdErrs = np.zeros(4000)
        
        VWAP = np.zeros(4000)
        ArrivalPrices = np.zeros(4000)
        TerminalPrices = np.zeros(4000)
        
        for i in range(1000):
            # Stock 1
            sigmas[i] = 0.3 + (np.random.rand() - np.random.rand()) * 0.03
            imbalances[i] = np.random.normal(0,1000)
            ADVs[i] = 12000 + (np.random.rand() - np.random.rand()) * 1000
            StdErrs[i] = 1
            
            # Stock 2
            sigmas[i+1000] = 0.3 + (np.random.rand() - np.random.rand()) * 0.03
            imbalances[i+1000] = np.random.normal(0,1000)
            ADVs[i+1000] = 12000 + (np.random.rand() - np.random.rand()) * 1000
            StdErrs[i+1000] = 2

            # Stock 3
            sigmas[i+2000] = 0.3 + (np.random.rand() - np.random.rand()) * 0.03
            imbalances[i+2000] = np.random.normal(0,1000)
            ADVs[i+2000] = 12000 + (np.random.rand() - np.random.rand()) * 1000
            StdErrs[i+2000] = 3

            # Stock 4
            sigmas[i+3000] = 0.3 + (np.random.rand() - np.random.rand()) * 0.03
            imbalances[i+3000] = np.random.normal(0,1000)
            ADVs[i+3000] = 12000 + (np.random.rand() - np.random.rand()) * 1000
            StdErrs[i+3000] = 4
            
        
        res = getOptimalEtaBeta(VWAP, ArrivalPrices, TerminalPrices, sigmas, imbalances, ADVs, StdErrs)
        
        print(res)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()