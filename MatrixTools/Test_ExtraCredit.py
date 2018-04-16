'''
Created on Apr 16, 2018

@author: Michael
'''
import unittest
import numpy as np
from MatrixTools.ExtraCreditCovariance import ExtraCreditCovariance

class Test(unittest.TestCase):


    def testExtraCredit(self):
        '''First we generate some fake data.'''
        L = np.array([[2, 0, 0],[1, 3, 0],[0.5, 0.4, 1]])
        print('True covariance is',np.dot(L,np.transpose(L)))
        
        Y = np.zeros((3, 10000))
        for i in range(10000):
            x1 = np.random.normal()
            x2 = np.random.normal()
            x3 = np.random.normal()
            
            Y[0,i] = 2*x1
            Y[1,i] = 1*x1+3*x2
            Y[2,i] = 0.5*x1+0.4*x2+1*x3
        
        C = ExtraCreditCovariance(Y)
        print('1-factor bias corrected PCA estimator of covariance is',C.getCovariance())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()