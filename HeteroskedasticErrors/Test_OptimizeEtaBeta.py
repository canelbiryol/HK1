import unittest
import numpy as np
from HeteroskedasticErrors.OptimizeEtaBeta import OptimizeEtaBeta

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
        X = np.zeros(4000)
        h = np.zeros(4000)
        
        eta = 3.0
        beta = 1.5
        
        for i in range(1000):
            # Stock 1
            sigmas[i] = 0.3 + (np.random.rand() - np.random.rand()) * 0.03
            imbalances[i] = np.random.normal(0,1000000)
            ADVs[i] = 30000 + (np.random.rand() - np.random.rand()) * 10000
            X[i] = abs(imbalances[i]) / (ADVs[i] * (6/6.5))
            StdErrs[i] = 1000
            
            # Stock 2
            sigmas[i+1000] = 0.6 + (np.random.rand() - np.random.rand()) * 0.06
            imbalances[i+1000] = np.random.normal(0,10000000)
            ADVs[i+1000] = 60000 + (np.random.rand() - np.random.rand()) * 10000
            X[i+1000] = abs(imbalances[i+1000]) / (ADVs[i+1000] * (6/6.5))
            StdErrs[i+1000] = 2000

            # Stock 3
            sigmas[i+2000] = 0.9 + (np.random.rand() - np.random.rand()) * 0.09
            imbalances[i+2000] = np.random.normal(0,1000000)
            ADVs[i+2000] = 90000 + (np.random.rand() - np.random.rand()) * 10000
            X[i+2000] = abs(imbalances[i+2000]) / (ADVs[i+2000] * (6/6.5))
            StdErrs[i+2000] = 3000

            # Stock 4
            sigmas[i+3000] = 1.2 + (np.random.rand() - np.random.rand()) * 0.12
            imbalances[i+3000] = np.random.normal(0,10000000)
            ADVs[i+3000] = 120000 + (np.random.rand() - np.random.rand()) * 10000
            X[i+3000] = abs(imbalances[i+3000]) / (ADVs[i+3000] * (6/6.5))
            StdErrs[i+3000] = 4000
            
            h[i] = eta * sigmas[i] * pow(X[i], beta) + StdErrs[i] * np.random.normal()
            h[i+1000] = eta * sigmas[i+1000] * pow(X[i+1000], beta) + StdErrs[i+1000] * np.random.normal()
            h[i+2000] = eta * sigmas[i+2000] * pow(X[i+2000], beta) + StdErrs[i+2000] * np.random.normal()
            h[i+3000] = eta * sigmas[i+3000] * pow(X[i+3000], beta) + StdErrs[i+3000] * np.random.normal()
        
        print(h)
        print(sigmas)
        print(imbalances)
        print(ADVs)
        print(StdErrs)
        
        optimizer = OptimizeEtaBeta()
        res = optimizer.getOptimalEtaBeta(h, sigmas, imbalances, ADVs, StdErrs)
        
        print(res)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()