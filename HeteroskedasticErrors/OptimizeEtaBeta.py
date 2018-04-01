'''
TODO: Write Spec
We assume heteroskedastic errors.
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
    """
    The residual sum of squares considering heteroskedastic errors
    StdErrors is the vector of STANDARD DEVIATIONS of the errors, not the variances
    X is the vector of [eta, beta] and h is the temporary impact
    """
    
    #Checks for consistency
    N = len(h)
    if (len(sigmas)!=N or len(imbalances)!=N or len(ADVs)!=N or len(StdErrs)!=N):
        raise Exception( 'All parameters should have the same length.' )
    for i in range(N):
        if StdErrs[i]<=1e-12:
            raise Exception( 'Standard errors must be strictly positive.' )
    if len(X)!=2:
        raise Exception( 'First parameter should be the vector [eta, beta].' )    
        
    eta = X[0]
    beta = X[1]
    
    RSS = 0
    for i in range(N):
        RSS += pow((h[i] - eta * sigmas[i] * pow(abs(imbalances[i]) / ((6/6.5) * ADVs[i]), beta)) / StdErrs[i], 2)
     
    #Return the reweighted RSS, normalized to account for heteroskedasticity
    return RSS

def jacobianRSS(X, h, sigmas, imbalances, ADVs, StdErrs):
    """
    The jacobian vector
    First element of return is partial of RSS w.r.t eta, second is partial of RSS w.r.t. beta
    """
    
    #Checks for consistency
    N = len(h)
    if (len(sigmas)!=N or len(imbalances)!=N or len(ADVs)!=N or len(StdErrs)!=N):
        raise Exception( 'All parameters should have the same length.' )
    for i in range(N):
        if StdErrs[i]<=1e-12:
            raise Exception( 'Standard errors must be strictly positive.' )
    if len(X)!=2:
        raise Exception( 'First parameter should be the vector [eta, beta].' )
    
    eta = X[0]
    beta = X[1]
    result = np.zeros(2)
    
    for i in range(N):
        factor = abs(imbalances[i]) / (ADVs[i] * (6/6.5))
        factorbeta = pow(factor, beta)
        factorbetam1 = pow(factor, beta -1)
        stderrsq = pow(StdErrs[i], 2)
        sigma = sigmas[i]
        hi = h[i]

        result[0] += sigma * factorbeta * (eta * sigma * factorbeta - hi) / stderrsq
        result[1] += beta * eta * sigma * factorbetam1 * (eta * sigma * factorbeta - hi) / stderrsq

    return(2 * result)
    
def getOptimalEtaBeta(VWAP, ArrivalPrices, TerminalPrices, sigmas, imbalances, ADVs, StdErrs):
    """Now the actual optimization code"""
    
    #Check for consistency
    N = len(VWAP)
    if (len(ArrivalPrices)!=N or len(TerminalPrices)!=N or len(sigmas)!=N or len(imbalances)!=N or len(ADVs)!=N or len(StdErrs)!=N):
        raise Exception('All inputs must have the same dimensionality.')
    
    # Almgren's values
    startPoint = np.array([0.142, 0.6])
    h = getTempImpact(VWAP, ArrivalPrices, TerminalPrices)
    
    optiResult = minimize(fun=RSS_hetero, x0=startPoint, args=(h, sigmas, imbalances, ADVs, StdErrs), method='BFGS', jac=jacobianRSS, options={'disp': True})
    #Print eta and beta
    return(optiResult.x)