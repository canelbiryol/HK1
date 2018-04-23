import numpy as np
from cvxopt import matrix
from cvxopt.solvers import qp, options
import pandas as pd
from HeteroskedasticErrors.StatsReader import StatsReader
# Display configurations
np.set_printoptions(threshold=50)



"""
Program implementing the Black-Litterman expected return estimator over one period of time.
"""



## Statistics
print('Reading statistics')

stats = StatsReader('/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/stats/stats.xlsx')
# Dimensionnality of the problem (tickers, days)
m, n = stats.getNumberOfTickers(), stats.getNumberOfDays()
# Sigmas
sigmas = stats.getStdErrorVector().reshape(m,n-1)

# Imbalances
imbalances = stats.getImbalanceVector().reshape(m,n-1)

# Average daily values
ADVs = stats.getADValuesVector().reshape(m,n-1)

# Volume weighted average prices
VWAPs = stats.getVWAPuntil400Vector()
VWAPsReshaped = stats.getVWAPuntil400Vector().reshape(m,n-1)



## Compute daily returns using VWAPs 
## Both arithmetic and logarithmic returns are computed
## with associated expectation vector/covariance matrices
print('Computing returns, expected returns and covariance matrices')

# Log returns and reshape into matrices
logReturns = np.empty((1, stats.getNumberOfTickers() * (stats.getNumberOfDays() - 1))).flatten()
logReturns[1:] = np.diff(np.log(VWAPs))
logReturns[0] = logReturns[1]
logReturns = np.reshape(logReturns, (stats.getNumberOfTickers(), stats.getNumberOfDays() - 1))

# Artihmetic returns and reshape into matrices
aritReturns = np.empty((1, stats.getNumberOfTickers() * (stats.getNumberOfDays() - 1))).flatten()
f_aritR = lambda ri, rf: (rf - ri) / ri
aritReturns[1:] = np.asarray([f_aritR(VWAPs[i], rf) for i,rf in enumerate(VWAPs[1:])])
aritReturns[0] = aritReturns[1]
aritReturns = np.reshape(aritReturns, (stats.getNumberOfTickers(), stats.getNumberOfDays() - 1))



## THEN: Create the toy problem. Solve for the max sharpe ratio portfolio before incorporating views.
def sampleFrontier(returns):

    returns = pd.DataFrame(returns)
    cov = np.matrix(np.cov(returns.T))
    N = returns.shape[1]
    pbar = np.matrix(returns.mean())
    
    
    # List of optimal mus for which we'll find the optimal sigmas
    optimal_mus = []
    # Minimum expected return
    r_min = pbar.mean()
    for i in range(50):
        optimal_mus.append(r_min)
        r_min += (pbar.mean() / 100)
    
    # Matices of the QP
    P = matrix(cov)
    q = matrix(np.zeros((N, 1)))
    G = matrix(np.concatenate((-np.array(pbar), -np.identity(N)), 0))
    A = matrix(1.0, (1,N))
    b = matrix(1.0)
    
    # List of optimal portfolio weights (frontier)
    options['show_progress'] = False
    optimal_weights = [qp(P, q, G, matrix(np.concatenate((-np.ones((1, 1)) * mu, np.zeros((N, 1))), 0)), A, b)['x'] for mu in optimal_mus]
    
    # Standard deviations
    optimal_sigmas = [np.sqrt(np.matrix(w).T * cov.T.dot(np.matrix(w)))[0,0] for w in optimal_weights]
    
    return r_min, optimal_weights, optimal_mus, optimal_sigmas

# Risk-free (proxy), and portfolio (weights, returns, stddev)
r_min, weightsList, returnsList, sigmasList = sampleFrontier(aritReturns.T)


def bestSharpe(r_min, sigmas, returns):
    # Max sharpe ratio
    best_sharpe = 0
    best_sharpe_index = 0
    for i,r in enumerate(returns):
        if ((r - r_min) / sigmas[i]) > best_sharpe:
            best_sharpe = (r - r_min) / sigmas[i]
            best_sharpe_index = i
    return(best_sharpe_index)
        
bestSharpeIndex = bestSharpe(r_min, sigmasList, returnsList)
sharpeW, sharpeR, sharpeS = np.array(weightsList[bestSharpeIndex]), returnsList[bestSharpeIndex], sigmasList[bestSharpeIndex]

print('Market portfolio daily returns:',  sharpeR)
print('Market portfolio daily std dev:', sharpeS)
print('Market portfolio weights:', sharpeW)

cov = np.matrix(np.cov(aritReturns))
equityRiskPremium = (sharpeR - r_min) / sharpeS**2
equilibriumExcessReturn = np.dot(np.dot(equityRiskPremium, cov), sharpeW)

## THEN: Incorporate views

# P and Q are the views matrix (for P: a 1 in line is an absolute view, a +1 and -1 is a relative view. Corresponding values in Q vector.)
# We incorporate 2 relative views in this toy problem.
P = np.zeros((2,m))
Q = np.random.uniform(low=0.005, high=0.40, size=(2,1)).flatten()

# View 1                      
P[0,0] = 1
P[0,1] = -1
# View 2
P[1,0] = 1
P[1,2] = -1
    
# tau is a scalar indicating the uncertainty in the CAPM (Capital Asset Pricing Model) prior
tau = 0.025

# omega represents the uncertainty of our views. Rather than specify the 'confidence'in one's view explicitly, we extrapolate an implied uncertainty from market parameters.
omega = np.dot(np.dot(np.dot(tau, P), cov), np.transpose(P))

# Compute equilibrium excess returns taking into account views on assets
sub_a = np.linalg.inv(np.dot(tau, cov))
sub_b = np.dot(np.dot(np.transpose(P), np.linalg.inv(omega)), P)
sub_c = np.dot(np.linalg.inv(np.dot(tau, cov)), equilibriumExcessReturn)
sub_d = np.dot(np.dot(np.transpose(P), np.linalg.inv(omega)), Q)

newEquilibriumExcessReturn = np.dot(np.linalg.inv(sub_a + sub_b), (sub_c + sub_d.T)).T     

def sampleFrontierBis(pbar, cov):

    N = pbar.shape[1]
    
    # List of optimal mus for which we'll find the optimal sigmas
    optimal_mus = []
    # Minimum expected return
    r_min = pbar.mean()
    for i in range(50):
        optimal_mus.append(r_min)
        r_min += (pbar.mean() / 100)
    
    # Matices of the QP
    P = matrix(cov)
    q = matrix(np.zeros((N, 1)))
    G = matrix(np.concatenate((-np.array(pbar), -np.identity(N)), 0))
    A = matrix(1.0, (1,N))
    b = matrix(1.0)
    
    # List of optimal portfolio weights (frontier)
    options['show_progress'] = False
    optimal_weights = [qp(P, q, G, matrix(np.concatenate((-np.ones((1, 1)) * mu, np.zeros((N, 1))), 0)), A, b)['x'] for mu in optimal_mus]
    
    # Standard deviations
    optimal_sigmas = [np.sqrt(np.matrix(w).T * cov.T.dot(np.matrix(w)))[0,0] for w in optimal_weights]
    
    return r_min, optimal_weights, optimal_mus, optimal_sigmas

## FINALLY: Perform a mean-variance optimization taking into account views
newR_min, newWeightsList, newReturnsList, newSigmasList = sampleFrontierBis(newEquilibriumExcessReturn + r_min, cov)

newBestSharpeIndex = bestSharpe(newR_min, newSigmasList, newReturnsList)

newSharpeW, newSharpeR, newSharpeS = np.array(weightsList[newBestSharpeIndex]), np.array(returnsList[newBestSharpeIndex]), np.array(sigmasList[newBestSharpeIndex])

print('Optimal weights with these views:', newSharpeW)
