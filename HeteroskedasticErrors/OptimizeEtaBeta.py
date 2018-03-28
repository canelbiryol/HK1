'''
Created on Mar 28, 2018

@author: Michael
'''

'''
We assume heterskedastic errors.
'''

import numpy as np
from scipy.optimize import minimize


def getTempImpact(VWAP, ArrivalPrices, TerminalPrices):
    """Calculates the vector of temporary impact, h"""
    #Checks for consistency
    N = len(VWAP)
    if (len(ArrivalPrices)!=N or len(TerminalPrices)!=N):
        raise Exception( 'All parameters should have the same length.' )
     
    return (VWAP-ArrivalPrices)-(TerminalPrices-ArrivalPrices)/2

def RSS_hetero(X, h, sigmas, imbalances, ADVs, StdErrs):
    """The residual sum of squares after considering heteroskedastic errors"""
    """StdErrors is the vector of STANDARD DEVIATIONS of the errors, not the variances"""
    """X is the vector of [eta, beta] and h is the temporary impact"""
    #Checks for consistency
    N = len(h)
    if (len(sigmas)!=N or len(imbalances)!=N or len(ADVs)!=N or len(StdErrs)!=N):
        raise Exception( 'All parameters should have the same length.' )
    for i in range(N):
        if StdErrs[i]<=1e-12:
            raise Exception( 'Standard errors must be strictly positive.' )
    if len(X)!=2:
        raise Exception( 'First parameter should be the vector [eta, beta].' )        
    #Return the reweighted RSS, normalized to account for heteroskedasticity
    eta = X[0]
    beta = X[1]
    
    RSS = 0
    for i in range(N):
        RSS += (h[i]-eta*sigmas[i]*((imbalances[i]*6.5/6/ADVs[i])**beta))**2/(StdErrs[i]*StdErrs[i])
     
    return RSS

def jacobianRSS(X, h, sigmas, imbalances, ADVs, StdErrs):
    """The jacobian vector"""
    """First element of return is partial of RSS w.r.t eta, second is partial of RSS w.r.t. beta"""
    #Checks for consistency
    N = len(h)
    if (len(sigmas)!=N or len(imbalances)!=N or len(ADVs)!=N or len(StdErrs)!=N):
        raise Exception( 'All parameters should have the same length.' )
    for i in range(N):
        if StdErrs[i]<=1e-12:
            raise Exception( 'Standard errors must be strictly positive.' )
    if len(X)!=2:
        raise Exception( 'First parameter should be the vector [eta, beta].' )
    
    result = np.zeros(2)
    for i in range(N):
        k = (imbalances[i]*6.5/ADVs[i]/6)
        eta = X[0]
        beta = X[1]
        result[0] += 2*sigmas[i]*(k**beta)*(eta*sigmas[i]*(k**beta)-h[i])/StdErrs[i]/StdErrs[i]
        result[1] += 2*beta*eta*sigmas[i]*(k**(beta-1))*(eta*sigmas[i]*(k**beta)-h[i])/StdErrs[i]/StdErrs[i]
    return result
    
'''Now the actual optimization code'''
def getOptimalEtaBeta(VWAP, ArrivalPrices, TerminalPrices, sigmas, imbalances, ADVs, StdErrs):
    #Check for consistency
    N = len(VWAP)
    if (len(ArrivalPrices)!=N or len(TerminalPrices)!=N or len(sigmas)!=N or len(imbalances)!=N or len(ADVs)!=N or len(StdErrs)!=N):
        raise Exception('All inputs must have the same dimensionality.')
    
    startPoint = np.array([0.142, 0.6])
    h= getTempImpact(VWAP, ArrivalPrices, TerminalPrices)
    
    results = minimize(RSS_hetero, startPoint,  h, sigmas, imbalances, ADVs, StdErrs, method='BFGS', jac=jacobianRSS, options={'disp': True})
    #Print eta and beta
    print(results.x)