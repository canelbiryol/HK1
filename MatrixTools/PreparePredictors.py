import numpy as np
import math

class PreparePredictors(object):
    '''
    Code that returns the g vector.
    Prepares the min variance predictor, omniscient predictor and random long-short predictor
    '''
    
    def __init__(self, outOfSampleStockReturns):
        '''
        Load the out-of-sample stock returns.
        outOfSampleStockReturns[i] is an array containing the returns of the ith stock.
        '''
        self.N = len(outOfSampleStockReturns)
        self.NormalizationFactor = math.sqrt(self.N)
        
        N_ticks = len(outOfSampleStockReturns[0])
        for k in outOfSampleStockReturns:
            if len(k)!=N_ticks:
                raise Exception('Each stock much have the same amount of input data.')
        
        
        '''For each stock compute the net return over the period'''
        self.netReturns = np.zeros(self.N)
        for x in range(self.N):
            netReturn = 1
            for y in range(N_ticks):
                if outOfSampleStockReturns[x][y]:
                    netReturn *= 1 + outOfSampleStockReturns[x][y]
            self.netReturns[x] = netReturn - 1
        
        ##Normalize
        self.netReturns = self.netReturns/np.linalg.norm(self.netReturns)
    
    def getMinVarPredictor(self):
        return np.ones(self.N)
        
    def getOmniscientPredictor(self):
        return self.NormalizationFactor*self.netReturns
    
    def getRandomPredictor(self):
        #Produce a random vector on the unit sphere
        random = np.random.rand(self.N)
        magnitude = 0
        for x in random:
            magnitude += x*x
        random /= math.sqrt(magnitude)
        
        return self.NormalizationFactor*random
        
        
        
        
        
        
        
        
        
        