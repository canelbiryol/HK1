import numpy as np
import pyRMT
from sklearn.covariance import ledoit_wolf
'''Class that produces the covariance matrices.
    Performs all the usual checks.
'''

class CovarianceCalculator(object):
    
    '''stockReturns[i] is an array containing the returns of the ith stock.
    '''
    def __init__(self, stockReturns):
        N_ticks = len(stockReturns[0])
        for k in stockReturns:
            if len(k)!=N_ticks:
                raise Exception('Each stock much have the same amount of input data.')
        
        self.stockReturns = stockReturns
        self.N_stocks = len(self.stockReturns)
        self.N_ticks = len(self.stockReturns[0])
        
    def getEmpiricalCovariance(self):
        return np.cov(self.stockReturns)
    
    def getClippedCovariance(self):
        return pyRMT.clipped(np.transpose(self.stockReturns), return_covariance=True)
    
    def getLedoitWolfCovariance(self):
        return ledoit_wolf(np.transpose(self.stockReturns))[0]
    
    


if __name__ == '__main__':
    pass