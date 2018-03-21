'''
Created on Mar 6, 2018

@author: Michael
'''
import unittest
import numpy as np
from Part_C.AutocorrelationPlotter import plotAutocorrelation

class Test_Autocorrelation_Plotter(unittest.TestCase):

    def testAutocorrelation(self):
        
        '''First let's make some fake data'''
        data = np.zeros(10000)
        data[0] = np.random.normal()
        data[1] = np.random.normal()
        data[2] = np.random.normal()
        data[3] = np.random.normal()
        for x in range(4,10000,1):
            data[x] = (
                (0.5+0.05*np.random.normal())*data[x-1]
                +(0.2+0.05*np.random.normal())*data[x-2]
                +(0.05+0.05*np.random.normal())*data[x-3]
                +(0.05+0.05*np.random.normal())*data[x-4]
                +0.1*np.random.normal())
        plotAutocorrelation(data, 5, 10)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()