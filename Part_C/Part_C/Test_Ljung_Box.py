'''
Created on Mar 6, 2018

@author: Michael
'''
import unittest
import numpy as np
from scipy.stats import chi2
from Part_C.Ljung_Box import Ljung_Box

class Test_Ljung_Box(unittest.TestCase):

    def testAutocorrelation(self):
        
        #First let's make some fake data with autocorrelation 0.5 at lag 1
        data = np.zeros(100000)
        data[0] = np.random.normal()
        for x in range(99999):
            data[x+1] = 0.5*data[x]+np.random.normal()
        K = Ljung_Box(data)
        #Print it out to check visually. Also verify it's close to 0.5
        print(K.getAutocorrelation(1))
        self.assertTrue( abs(K.getAutocorrelation(1)-0.5)<0.01 )
        print('Autocorrelation function works.')
        print()
    
    def testQuantile(self):
        '''
        Now let's check the Ljung-Box statistic.
        Start with data having autocorrelation at lag 5.
        '''
        data = np.zeros(10000)
        data[0] = np.random.normal()
        data[1] = np.random.normal()
        data[2] = np.random.normal()
        data[3] = np.random.normal()
        data[4] = np.random.normal()
        for x in range(5,10000,1):
            '''Make the data noisy'''
            data[x] = (0.6+np.random.normal(0,0.1))*data[x-5]+0.2*np.random.normal()
        K = Ljung_Box(data)
        
        C = np.zeros(5)
        Q = 0
        for x in range(5):
            C[x] = K.getAutocorrelation(x+1)
            print('The autocorrelation at lag',x+1,'is',C[x])
            Q += C[x]*C[x]/(10000-x-1)
        Q *= 10000*10002
        print()
        
        #Check the getQuantile produces an accurate chi2 cdf quantile compared to the manual calculation
        self.assertTrue(abs(chi2.cdf(Q,5)-K.getQuantile(5))<0.001)

        self.assertTrue(K.getQuantile(5)>0.95)
        print('We reject the null hypothesis that the data is independent up to lag 5 at 95% confidence.')
        print('i.e. there is autocorrelation at lag 5')
        self.assertTrue(K.getQuantile(4)<0.95)
        print('We do not reject the hypothesis that the data is independent up to lag 4 at 95% confidence.')
        print('i.e. there is no autocorrelation at lag 4')
        print('Ljung-Box test statistic works.')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()