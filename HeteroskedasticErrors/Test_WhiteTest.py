import unittest
import numpy as np
from HeteroskedasticErrors.WhiteTestHomoskedasticity import WhiteTestHomoskedasticity

class Test_WhiteTest(unittest.TestCase):
    '''
    Class allowing testing White test's implementation.
    '''
    
    def test1(self):
        y = np.ones(1000)
        residuals = np.zeros(1000)
        residuals[:100] = 0.5
        degreesOfFreedom = 66
        wTest = WhiteTestHomoskedasticity(y, residuals, degreesOfFreedom)
        
        print(wTest.getCoefficients())
        print(wTest.getRSquared())
        print(wTest.getPValue())
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()