from math import sqrt
import numpy as np

class GetStdDev(object):
    '''
    Back out the residuals' standard deviation from Almgren's values.
    For a given stock, it is assumed to be constant over the timeframe.
    Could also be done via bootstrapping.
    '''

    def __init__(self, h, sigmas, imbalances, ADVs, Ndays=65, eta0=0.142, beta0=0.6):
        
        res = h - eta0 * sigmas * pow((abs(imbalances) / (ADVs * (6/6.5))), beta0)
        
        length = len(res)
        modulo = length // Ndays
        
        average_std = lambda xarr: sqrt(sum(np.power(xarr, 2))/len(xarr))
        
        print(np.array([average_std(np.array(res[i * Ndays : (i+1) * Ndays])) for i in range(0, modulo)]).flatten())
        
        self._arrays_std = np.array([np.tile(average_std(np.array(res[i * Ndays : (i+1) * Ndays])), (Ndays, 1)) for i in range(0, modulo)]).flatten()
        
    def getLambdasVector(self):
        return(self._arrays_std)
