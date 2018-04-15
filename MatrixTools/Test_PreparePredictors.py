'''
Created on Apr 15, 2018

@author: Michael
'''
import unittest
import numpy as np
from MatrixTools.PreparePredictors import PreparePredictors
from wheel.signatures import assertTrue


class Test(unittest.TestCase):


    def testPreparePredictors(self):
        '''Prepare some fake data. 3 stocks. One with net 10% growth, 20% and 30%'''
        outOfSampleStockReturns = np.array([[0, 0, -0.5, 1, 0.1],[0, 3, 0, -0.75, 0.2],[-0.5, 0, 0, 1, 0.3]])
        P = PreparePredictors(outOfSampleStockReturns)
        print('Minimum Variance Predictor is', P.getMinVarPredictor())
        print('Omniscient Predictor is', P.getOmniscientPredictor())
        K = P.getRandomPredictor()
        print('Random Predictor is', K)
        
        tol = 0.00000001
        '''Check the 2-norm of all vectors is sqrt(3)'''
        assertTrue(abs(np.linalg.norm(K)*np.linalg.norm(K)-3)<tol)
        assertTrue(abs(np.linalg.norm(P.getOmniscientPredictor())*np.linalg.norm(P.getOmniscientPredictor())-3)<tol)
        assertTrue(abs(np.linalg.norm(P.getMinVarPredictor())*np.linalg.norm(P.getMinVarPredictor())-3)<tol)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()