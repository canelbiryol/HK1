from math import sqrt
import numpy as np
from HeteroskedasticErrors.OptimizeEtaBeta import OptimizeEtaBeta

class GetStdDev(object):
    '''
    Back out the residuals' standard deviation from Almgren's values.
    For a given stock, it is assumed to be constant over the timeframe.
    Could also be done via bootstrapping.
    '''

    def __init__(self, h, sigmas, imbalances, ADVs, Ndays=65):
        
        self._h = h
        self._sigmas = sigmas
        self._imbalances = imbalances
        self._ADVs = ADVs
        self._Ndays = Ndays
        
        self._arrays_std = []
        
    def getLambdasVectorOneStep(self, eta0=0.142, beta0=0.6):
        
        res = self._h - eta0 * self._sigmas * pow((abs(self._imbalances) / (self._ADVs * (6/6.5))), beta0)
        
        length = len(res)
        modulo = length // self._Ndays
        
        average_std = lambda xarr: sqrt(sum(np.power(xarr, 2))/len(xarr))
        
        #print(np.array([average_std(np.array(res[i * Ndays : (i+1) * Ndays])) for i in range(0, modulo)]).flatten())
        self._arrays_std = np.array([np.tile(average_std(np.array(res[i * self._Ndays : (i+1) * self._Ndays])), (self._Ndays, 1)) for i in range(0, modulo)]).flatten()

        return(self._arrays_std)
    
    def getLambdasVectorOneStepHomo(self):
        # Start from homoskedastic errors
        stdErrs = np.ones(self._ADVs.shape)
        
        # Get optimal values for eta and beta for this homoskedastic case (starting point)
        optimizer = OptimizeEtaBeta()
        etaBetaVector = optimizer.getOptimalEtaBeta(self._h, self._sigmas, self._imbalances, self._ADVs, stdErrs).x
        
        # Get corresponding errors
        stdErrs = self.getLambdasVectorOneStep(etaBetaVector[0], etaBetaVector[1])
        
        return(stdErrs)