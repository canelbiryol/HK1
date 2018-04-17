import numpy as np
import math

class ExtraCreditCovariance(object):
    '''
    classdocs
    '''
    def __init__(self, stockReturns):
        '''Similar to before, stockReturns should be a (NxT) matrix'''
        N_ticks = len(stockReturns[0])
        for k in stockReturns:
            if len(k)!=N_ticks:
                raise Exception('Each stock much have the same amount of input data.')
        
        self.stockReturns = stockReturns
        self.N = len(self.stockReturns)
        self.T = len(self.stockReturns[0])
        
        
    def getCovariance(self):
        
        S = np.dot(self.stockReturns,np.transpose(self.stockReturns))/self.T
        W,V = np.linalg.eig(S)
        z = np.ones(self.N)/math.sqrt(self.N)
        betaHat = np.sign(np.dot(V[:,0],z))*V[:,0]
        sigma2Hat = W[0]
        stockSpecificVariance = np.diag(np.diag(S-sigma2Hat*np.outer(betaHat, betaHat)))
        Delta = np.diag(np.diag(stockSpecificVariance)**(-0.5))
        
        updatedSigma2Hat = sigma2Hat*np.dot(np.matmul(Delta, betaHat), np.matmul(Delta, betaHat))
        updatedS = np.matmul(Delta, np.matmul(S, Delta))
        updatedz = np.matmul(Delta, z)/np.linalg.norm(np.matmul(Delta, z))
        updatedBeta = np.matmul(Delta, betaHat)/np.linalg.norm(np.matmul(Delta, betaHat))
        
        delta2_shrinkage = (np.matrix.trace(updatedS)-updatedSigma2Hat)/(self.N-1-self.N/self.T)
        c_shrinkage = self.N/(self.T*updatedSigma2Hat-self.N*delta2_shrinkage)
        f_shrinkage = 1+delta2_shrinkage*c_shrinkage
        
        shrinkage_parameter = (f_shrinkage + 1/f_shrinkage)*(f_shrinkage*np.dot(updatedBeta, updatedz))/(1-(f_shrinkage*np.dot(updatedBeta, updatedz))**2)
        shrunkBeta = (betaHat+shrinkage_parameter*z)/math.sqrt(1+2*shrinkage_parameter*np.dot(betaHat,z)+shrinkage_parameter**2)
        shrunkSigma2Hat = sigma2Hat*(np.dot(betaHat,z)**2)/(np.dot(shrunkBeta,z)**2)
        shrunkDelta = np.diag(np.diag(S-shrunkSigma2Hat*np.outer(shrunkBeta, shrunkBeta)))
        
        return shrunkSigma2Hat*np.outer(shrunkBeta, shrunkBeta)+shrunkDelta
        
        
        
    

        