import unittest
import numpy as np
from HeteroskedasticErrors.StandardErrorsEtaBeta import StandardErrorEtaBeta

class Test_StandardErrorsEtaBeta(unittest.TestCase):

    def test1(self):
        '''
        Test to see if our GetStdDev code works
        First let's create some fake data in a universe of 1000 days and 4 stocks.
        The stocks have similar behaviors and different StdErrs to account for heteroskedasticity.
        We try to retrieve the standard deviations of the residuals
        '''
        
        ## First calculation with very big sample size. Should be a good estimate.
        print("First calculation, sample of size 400000")
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
        
        
        stdDevCalculator = StandardErrorEtaBeta([eta, beta], sigmas, imbalances, ADVs, StdErrs)
        
        print(stdDevCalculator.getCovarianceMatrix())
        
        ## Second calculation, with smaller sample test. Covariances should be larger now.
        print("Second calculation, sample of size 40000. Relatively larger covariances expected")
        sigmas = np.zeros(40000)
        imbalances = np.zeros(40000)
        ADVs = np.zeros(40000)
        StdErrs = np.zeros(40000)
        X = np.zeros(40000)
        h = np.zeros(40000)
        
        eta = 3.0
        beta = 1.5
        
        for i in range(10000):
            # Stock 1
            sigmas[i] = 0.3 + (np.random.rand() - np.random.rand()) * 0.03
            imbalances[i] = np.random.normal(0,100000)
            ADVs[i] = 30000 + (np.random.rand() - np.random.rand()) * 10000
            X[i] = abs(imbalances[i]) / (ADVs[i] * (6/6.5))
            StdErrs[i] = 1000
            
            # Stock 2
            sigmas[i+10000] = 0.6 + (np.random.rand() - np.random.rand()) * 0.06
            imbalances[i+10000] = np.random.normal(0,1000000)
            ADVs[i+10000] = 60000 + (np.random.rand() - np.random.rand()) * 10000
            X[i+10000] = abs(imbalances[i+10000]) / (ADVs[i+10000] * (6/6.5))
            StdErrs[i+10000] = 2000

            # Stock 3
            sigmas[i+20000] = 0.9 + (np.random.rand() - np.random.rand()) * 0.09
            imbalances[i+20000] = np.random.normal(0,100000)
            ADVs[i+20000] = 90000 + (np.random.rand() - np.random.rand()) * 10000
            X[i+20000] = abs(imbalances[i+20000]) / (ADVs[i+20000] * (6/6.5))
            StdErrs[i+20000] = 3000

            # Stock 4
            sigmas[i+30000] = 1.2 + (np.random.rand() - np.random.rand()) * 0.12
            imbalances[i+30000] = np.random.normal(0,1000000)
            ADVs[i+30000] = 120000 + (np.random.rand() - np.random.rand()) * 10000
            X[i+30000] = abs(imbalances[i+30000]) / (ADVs[i+30000] * (6/6.5))
            StdErrs[i+30000] = 4000
            
            h[i] = eta * sigmas[i] * pow(X[i], beta) + StdErrs[i] * np.random.normal()
            h[i+10000] = eta * sigmas[i+10000] * pow(X[i+10000], beta) + StdErrs[i+10000] * np.random.normal()
            h[i+20000] = eta * sigmas[i+20000] * pow(X[i+20000], beta) + StdErrs[i+20000] * np.random.normal()
            h[i+30000] = eta * sigmas[i+30000] * pow(X[i+30000], beta) + StdErrs[i+30000] * np.random.normal()
        
        
        stdDevCalculator = StandardErrorEtaBeta([eta, beta], sigmas, imbalances, ADVs, StdErrs)
        
        print(stdDevCalculator.getCovarianceMatrix())


        ## Third and last calculation with ridiculously small sample. Should be very large now.
        print("Last calculation, sample of size 80. Relatively much larger covariances expected")
        sigmas = np.zeros(80)
        imbalances = np.zeros(80)
        ADVs = np.zeros(80)
        StdErrs = np.zeros(80)
        X = np.zeros(80)
        h = np.zeros(80)
        
        eta = 3.0
        beta = 1.5
        
        for i in range(20):
            # Stock 1
            sigmas[i] = 0.3 + (np.random.rand() - np.random.rand()) * 0.03
            imbalances[i] = np.random.normal(0,1000000)
            ADVs[i] = 30000 + (np.random.rand() - np.random.rand()) * 10000
            X[i] = abs(imbalances[i]) / (ADVs[i] * (6/6.5))
            StdErrs[i] = 1000
            
            # Stock 2
            sigmas[i+20] = 0.6 + (np.random.rand() - np.random.rand()) * 0.06
            imbalances[i+20] = np.random.normal(0,10000000)
            ADVs[i+20] = 60000 + (np.random.rand() - np.random.rand()) * 10000
            X[i+20] = abs(imbalances[i+20]) / (ADVs[i+20] * (6/6.5))
            StdErrs[i+20] = 2000

            # Stock 3
            sigmas[i+40] = 0.9 + (np.random.rand() - np.random.rand()) * 0.09
            imbalances[i+40] = np.random.normal(0,1000000)
            ADVs[i+40] = 90000 + (np.random.rand() - np.random.rand()) * 10000
            X[i+40] = abs(imbalances[i+40]) / (ADVs[i+40] * (6/6.5))
            StdErrs[i+40] = 3000

            # Stock 4
            sigmas[i+60] = 1.2 + (np.random.rand() - np.random.rand()) * 0.12
            imbalances[i+60] = np.random.normal(0,10000000)
            ADVs[i+60] = 120000 + (np.random.rand() - np.random.rand()) * 10000
            X[i+60] = abs(imbalances[i+60]) / (ADVs[i+60] * (6/6.5))
            StdErrs[i+60] = 4000
            
            h[i] = eta * sigmas[i] * pow(X[i], beta) + StdErrs[i] * np.random.normal()
            h[i+20] = eta * sigmas[i+20] * pow(X[i+20], beta) + StdErrs[i+20] * np.random.normal()
            h[i+40] = eta * sigmas[i+40] * pow(X[i+40], beta) + StdErrs[i+40] * np.random.normal()
            h[i+60] = eta * sigmas[i+60] * pow(X[i+60], beta) + StdErrs[i+60] * np.random.normal()
        
        
        stdDevCalculator = StandardErrorEtaBeta([eta, beta], sigmas, imbalances, ADVs, StdErrs)
        
        print(stdDevCalculator.getCovarianceMatrix())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()