'''
Created on Mar 6, 2018

@author: Michael
'''
import numpy as np
from partB.xMinuteReturn import getXSecTradeReturns, getXSecMidQuoteReturns
from Part_C.Ljung_Box import Ljung_Box
from array import array

class BucketSizeOptimizer(object):
    
    def __init__(self, dataSet):
        '''Stores the data set inside the class to perform the analysis'''
        self.dataSet = dataSet
        '''We test buckets of 10s, 30s, 1m, 5m, 10m, 15m, 30m'''
        self.buckets = array([10, 30, 60, 300, 600, 900, 1800])   
    
    def changeDataSet(self, newDataSet):
        '''Allows the user to change the data set'''
        self.dataSet = newDataSet
    
    def loadNewBuckers(self, newBuckets):
        '''Allows the user to change the data set'''
        self.buckets = np.asarray(newBuckets)
    
    def optimize(self, n_lags, confidence, isTrade=True):
        if isTrade == True:
            print('Optimizing over TRADES.')
        elif isTrade == False :
            print('Optimizing over MIDQUOTES.')
        
        for x in range(len(self.buckets)):
            if isTrade == False:
                '''For dealing with quotes'''
                prepared_data = getXSecMidQuoteReturns(self.dataSet, self.buckets[x])
            else:
                prepared_data = getXSecTradeReturns(self.dataSet, self.buckets[x])
            
            LB = Ljung_Box(prepared_data)
            if LB.getQuantile(n_lags)<confidence:
                '''This means no serial autocorrelation when testing up to lag 20.
                    We can stop here and do not need to increase the window size'''
                print('Optimal window size found to be',self.buckets[x],'seconds.')
                return self.buckets[x]
        '''If we get to the end, we notify the user to load new buckets'''
        print('All bucket sizes exhibit serial autocorrelation. Load a new set of window sizes greater than', self.buckets[len(self.buckets)-1], 'seconds.')
