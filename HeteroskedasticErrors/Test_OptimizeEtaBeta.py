'''
Created on Mar 29, 2018

@author: Louis
'''
import unittest
import numpy as np

class Test(unittest.TestCase):


    def test1(self):
        '''
        Test to see if our OptimizeEtaBeta code works
        First let's create some fake data in a universe of 1000 days and 4 stocks.
        The stocks have similar behaviors and different StdErrs to account for heteroskedasticity.
        '''
        
        h = np.zeros(4000)
        sigmas = np.zeros(4000)
        imbalances = np.zeros(4000)
        ADVs = np.zeros(4000)
        StdErrs = np.zeros(4000)

        for i in range(1000):
            sigmas[i] = 0.3 + np.random.rand()*0.03 - np.random.rand()*0.03
            imbalances[i] = np.random.normal(0,1000)
            ADVs[i] = 12000 + np.random.rand()*1000 - np.random.rand()*1000
            StdErrs[i] = 1
        for i in range(1000,0000,1):
            sigmas[i] = 0.3 + np.random.rand()*0.03 - np.random.rand()*0.03
            imbalances[i] = np.random.normal(0,1000)
            ADVs[i] = 12000 + np.random.rand()*1000 - np.random.rand()*1000
            StdErrs[i] = 1            


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()