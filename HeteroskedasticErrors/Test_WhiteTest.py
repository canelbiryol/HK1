import unittest
import numpy as np
from HeteroskedasticErrors.WhiteTestHomoskedasticity import WhiteTestHomoskedasticity

class Test_WhiteTest(unittest.TestCase):
    '''
    Class allowing testing White test's implementation.
    '''
    
    def test1(self):
        
        print("Generating heteroskedastic data.")
        noise = np.random.normal(size=100)
        
        residuals = np.zeros(1000)
        residuals[:100] = 0.5 * noise
        residuals[100:200] = 1 * noise
        residuals[200:300] = 1.5 * noise
        residuals[300:400] = 2 * noise
        residuals[400:500] = 2.5 * noise
        residuals[500:600] = 3 * noise
        residuals[600:700] = 3.5 * noise
        residuals[700:800] = 4 * noise
        residuals[800:900] = 4.5 * noise
        residuals[900:1000] = 5 * noise
        degreesOfFreedom = 10
        wTest = WhiteTestHomoskedasticity(residuals, degreesOfFreedom)

        pValue = wTest.getPValue()
        
        print("pValue with a small number of observation:", pValue)

        noise = np.random.normal(size=1000)
        
        residuals = np.zeros(10000)
        residuals[:1000] = 0.5 * noise
        residuals[1000:2000] = 1 * noise
        residuals[2000:3000] = 1.5 * noise
        residuals[3000:4000] = 2 * noise
        residuals[4000:5000] = 2.5 * noise
        residuals[5000:6000] = 3 * noise
        residuals[6000:7000] = 3.5 * noise
        residuals[7000:8000] = 4 * noise
        residuals[8000:9000] = 4.5 * noise
        residuals[9000:10000] = 5 * noise
        degreesOfFreedom = 10
        wTest = WhiteTestHomoskedasticity(residuals, degreesOfFreedom)

        pValue = wTest.getPValue()
        
        print("pValue with a big number of observation (expected to be much lower since data is indeed heteroskedastic):", pValue)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()