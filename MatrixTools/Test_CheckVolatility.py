import unittest
import numpy as np
from MatrixTools.PreparePredictors import PreparePredictors
from MatrixTools.CheckVolatility import CheckVolatility, getWeights
from MatrixTools.CovarianceMatrices import CovarianceCalculator

class Test(unittest.TestCase):


    def testCheckVolatility(self):
        '''Create some fake returns with a specified mean/variance stucture'''
        Mean = np.array([1, 1, 1])
        Variance = np.array([[2, 2, 0], [2, 4, 0], [0, 0, 1]])
        training = [None]*10000
        testing = [None]*10000
        for i in range(10000):
            training[i] = np.random.multivariate_normal(Mean, Variance)
            testing[i] = np.random.multivariate_normal(Mean, Variance)
            
        '''IMPORTANT: Make sure the returns are a (N_stocks, N_ticks) array.'''
        training = np.transpose(training)
        testing = np.transpose(testing)
        
        '''Get the Covariance Matrix estimate.
        It should look similar to our covariance matrix.'''
        K = CovarianceCalculator(training)
        CovMatEstimate = K.getEmpiricalCovariance()
        print(CovMatEstimate)
        
        '''Use the Min Var predictor. Doesn't matter what argument we pass here.'''
        P = PreparePredictors(training)
        MinVarPredictor = P.getMinVarPredictor()
        
        '''The Min Var portfolio should look like [1/3, 0, 2/3]'''
        print(getWeights(Variance, MinVarPredictor))
        
        C = CheckVolatility(testing)
        '''The square of our volatility estimate should be close to the 
            variance of the minimum variance portfolio, which is 0.6666.'''
        print(C.checkVolatility(CovMatEstimate, MinVarPredictor)**2)
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCheckVolatility']
    unittest.main()