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
        
        X = [1.,1.]
        sigmas = (np.random.random((1000, 1))).flatten() * pow(10,-2)
        imbalances = (np.random.random((1000, 1))).flatten() * pow(10,4)
        ADVs = (np.random.random((1000, 1))).flatten() * pow(10,5)
        StdErrs = (np.random.random((1000, 1))).flatten() * pow(10,-3)
        
        stdDevCalculator = StandardErrorEtaBeta(X, sigmas, imbalances, ADVs, StdErrs)
        
        # Order of magnitude expected : 10^-5, 10^-6 or 10^-7
        print(stdDevCalculator.getCovarianceMatrix())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()