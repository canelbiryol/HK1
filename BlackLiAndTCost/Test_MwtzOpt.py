import unittest
import numpy as np
import scipy.optimize

class Test_MwtzOpt(unittest.TestCase):

    def testStats(self):
        
        # Variance + penalty
        def fitnessMetric(W, R, C, r):
            # For given level of return r, find weights which minimizes portfolio variance.
            mean_1, var = np.sum(R*W), np.dot(np.dot(W, C), W)
            # Penalty for not meeting stated portfolio return effectively serves as optimization constraint
            # Here, r is the 'target' return
            penalty = 0.1*abs(mean_1-r)
            return var + penalty
        
        # Mean variance optimal portfolio
        def markowitzWeights(R, C):
            n = len(R)
            W = np.ones([n])/n # Start with equal weights
            b_ = [(0.1,1) for i in range(n)] # Bounds (decision variables)
            c_ = ({'type':'eq', 'fun': lambda W: np.sum(W)-1. }) # weights must sum to 1 (constraint)
            # 'target' return is the expected return on the market portfolio
            optimized = scipy.optimize.minimize(fitnessMetric, W, (R, C, sum(R*W)), method='SLSQP', constraints=c_, bounds=b_)
            if not optimized.success:
                raise BaseException(optimized.message)
            return optimized.x 

        R = np.array([0.03,0.08,-0.02])
        C = np.matrix([[0.25,1.0,0.5],[0.25,1.0,0.5],[0.25,1.0,0.5]])

        res = markowitzWeights(R, C)
        print(res)
        
        self.assertAlmostEquals( res[0], 0.8, 2 )
        self.assertAlmostEquals( res[1], 0.1, 2 )
        self.assertAlmostEquals( res[2], 0.1, 2 )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testVWAP']
    unittest.main()