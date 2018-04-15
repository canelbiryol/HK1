'''
Created on Apr 14, 2018

@author: Michael
'''
import numpy as np
import math 

class CheckVolatility(object):
    
    def __init__(self, outOfSampleStockReturns):
        
        '''outOfSampleStockReturns[i] is an array containing the returns of the ith stock.
        '''
        self.N = len(outOfSampleStockReturns)
        self.outOfSampleStockReturns = outOfSampleStockReturns
        self.N_ticks = len(outOfSampleStockReturns[0])
        for k in outOfSampleStockReturns:
            if len(k)!=self.N_ticks:
                raise Exception('Each stock much have the same amount of input data.')
    
    def checkVolatility(self, CovMat, Predictor):
        W = getWeights(CovMat,Predictor)
        returns = np.zeros(self.N_ticks)
        for x in range(self.N_ticks):
            returns[x] = np.dot(W,self.outOfSampleStockReturns[:,x])
        return math.sqrt(np.cov(returns, ddof=1))
    
        
def getWeights(CovMat, Predictor):
    N = len(Predictor)
    if CovMat.shape[0]!=N or CovMat.shape[1]!=N:
        raise Exception('Check Covariance Matrix and Predictor.')
    S = np.linalg.inv(CovMat)
    return np.dot(S,Predictor)/(np.dot(np.transpose(Predictor),np.dot(S,Predictor)))
    
    
    

        