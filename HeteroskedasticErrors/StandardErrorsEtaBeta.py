import numpy as np
from math import log

class StandardErrorEtaBeta(object):
    '''
    Compute the standard error vector of eta and beta after linearization of the model:
    Var(eta^,beta^) = (J^T J)^-1 * (J^T W J) * (J^T J)^-1
    (So-called sandwich formula)
    '''

    def __init__(self, X, sigmas, imbalances, ADVs, StdErrs):
        '''self._X is the vector [eta, beta]'''
        
        self._X = X
        self._sigmas = sigmas
        self._imbalances = imbalances
        self._ADVs = ADVs
        self._StdErrs = StdErrs

        #Checks for consistency
        N = len(self._sigmas)
        if (len(self._imbalances)!=N or len(self._ADVs)!=N or len(self._StdErrs)!=N):
            print(len(self._imbalances), len(self._ADVs), len(self._StdErrs))
            raise Exception( 'All parameters should have the same length.' )
        for i in range(N):
            if self._StdErrs[i]<=1e-12:
                raise Exception( 'Standard errors must be strictly positive.' )
        if len(self._X)!=2:
            raise Exception( 'First parameter should be the vector [eta, beta].' )

    def getCovarianceMatrix(self):
    
        N = len(self._sigmas)
        eta = self._X[0]
        beta = self._X[1]
        
        #Calculate J matrix
        J = np.zeros((N,2))
        for i in range(N):
            factor = abs(self._imbalances[i]) / (self._ADVs[i] * (6/6.5))
            J[i,0] = pow(factor, beta) * self._sigmas[i]
            J[i,1] = eta * self._sigmas[i] * log(factor) * pow(factor, beta)
        
        """
        W = np.zeros((N,1))
        for i in range(N):
            W[i,0] = pow(self._StdErrs[i], 2)
            
        print(W)
        """
        
        WJ = np.zeros((N,2))
        norm = 0
        for i in range(N):
            norm += pow(self._StdErrs[i], 2)
            WJ[i,0] = pow(self._StdErrs[i], 2) * J[i,0]
            WJ[i,1] = pow(self._StdErrs[i], 2) * J[i,1]
        WJ = WJ / norm
        
        M = np.linalg.inv(np.dot(np.transpose(J),J))
        R = np.dot(np.transpose(J), WJ)
        
        return(np.dot(M, np.dot(R, M)))
