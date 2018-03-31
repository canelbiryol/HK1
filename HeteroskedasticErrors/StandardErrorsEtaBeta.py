'''

'''
import numpy as np

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
        k = imbalances[i]*6.5/ADVs[i]/6
        J[i,0] = k**beta*sigmas[i]
        J[i,1] = beta*eta*sigmas[i]*(k**(beta-1))

    W = np.zeros((N,N))
    for i in range(N):
        W[i,i] = StdErrs[i]*StdErrs[i]
    
    M = np.linalg.inv(np.dot(np.transpose(J),J))
    R = np.dot(np.transpose(J), np.dot(W, J))
    
    result = np.dot(M, np.dot(R, M))
    
    return result