import unittest
import numpy as np
from HeteroskedasticErrors.GetStdDev import GetStdDev

class Test_OptimizeEtaBeta(unittest.TestCase):

    def test1(self):
        '''
        Test to see if our GetStdDev code works
        First let's create some fake data in a universe of 1000 days and 4 stocks.
        The stocks have similar behaviors and different StdErrs to account for heteroskedasticity.
        We try to retrieve the standard deviations of the residuals
        '''
        
        sigmas = np.zeros(400000)
        imbalances = np.zeros(400000)
        ADVs = np.zeros(400000)
        StdErrs = np.zeros(400000)
        X = np.zeros(400000)
        h = np.zeros(400000)
        
        eta = 3.0
        beta = 1.5
        
        for i in range(100000):
            # Stock 1
            sigmas[i] = 0.3 + (np.random.rand() - np.random.rand()) * 0.03
            imbalances[i] = np.random.normal(0,1000000)
            ADVs[i] = 30000 + (np.random.rand() - np.random.rand()) * 10000
            X[i] = abs(imbalances[i]) / (ADVs[i] * (6/6.5))
            StdErrs[i] = 1000
            
            # Stock 2
            sigmas[i+100000] = 0.6 + (np.random.rand() - np.random.rand()) * 0.06
            imbalances[i+100000] = np.random.normal(0,10000000)
            ADVs[i+100000] = 60000 + (np.random.rand() - np.random.rand()) * 10000
            X[i+100000] = abs(imbalances[i+100000]) / (ADVs[i+100000] * (6/6.5))
            StdErrs[i+100000] = 2000

            # Stock 3
            sigmas[i+200000] = 0.9 + (np.random.rand() - np.random.rand()) * 0.09
            imbalances[i+200000] = np.random.normal(0,1000000)
            ADVs[i+200000] = 90000 + (np.random.rand() - np.random.rand()) * 10000
            X[i+200000] = abs(imbalances[i+200000]) / (ADVs[i+200000] * (6/6.5))
            StdErrs[i+200000] = 3000

            # Stock 4
            sigmas[i+300000] = 1.2 + (np.random.rand() - np.random.rand()) * 0.12
            imbalances[i+300000] = np.random.normal(0,10000000)
            ADVs[i+300000] = 120000 + (np.random.rand() - np.random.rand()) * 10000
            X[i+300000] = abs(imbalances[i+300000]) / (ADVs[i+300000] * (6/6.5))
            StdErrs[i+300000] = 4000
            
            h[i] = eta * sigmas[i] * pow(X[i], beta) + StdErrs[i] * np.random.normal()
            h[i+100000] = eta * sigmas[i+100000] * pow(X[i+100000], beta) + StdErrs[i+100000] * np.random.normal()
            h[i+200000] = eta * sigmas[i+200000] * pow(X[i+200000], beta) + StdErrs[i+200000] * np.random.normal()
            h[i+300000] = eta * sigmas[i+300000] * pow(X[i+300000], beta) + StdErrs[i+300000] * np.random.normal()
        
        res = GetStdDev(h, sigmas, imbalances, ADVs, Ndays=100000).getLambdasVectorOneStep(eta0=3.0, beta0=1.5)
        
        # Expected (approximately): 1000, 2000, 3000, 4000
        print(res)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()