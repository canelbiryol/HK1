import numpy as np
from math import log

'''
TODO: Write Spec
'''

def getCovarianceMatrix(X, sigmas, imbalances, ADVs, StdErrs):
    '''X is the vector [eta, beta]'''

    #Checks for consistency
    N = len(sigmas)
    if (len(imbalances)!=N or len(ADVs)!=N or len(StdErrs)!=N):
        raise Exception( 'All parameters should have the same length.' )
    for i in range(N):
        if StdErrs[i]<=1e-12:
            raise Exception( 'Standard errors must be strictly positive.' )
    if len(X)!=2:
        raise Exception( 'First parameter should be the vector [eta, beta].' )
    
    eta = X[0]
    beta = X[1]
    
    #Calculate J matrix
    J = np.zeros((N,2))
    for i in range(N):
        factor = imbalances[i] / (ADVs[i] * (6/6.5))
        J[i,0] = pow(factor, beta) * sigmas[i]
        J[i,1] = eta * sigmas[i] * log(factor) * pow(factor, beta)

    W = np.zeros((N,N))
    for i in range(N):
        W[i,i] = pow(StdErrs[i], 2)
    
    M = np.linalg.inv(np.dot(np.transpose(J),J))
    R = np.dot(np.transpose(J), np.dot(W, J))
    
    return(np.dot(M, np.dot(R, M)))    
