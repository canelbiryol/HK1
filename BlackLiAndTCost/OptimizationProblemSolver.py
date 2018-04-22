import numpy as np
from cvxopt import matrix
from cvxopt.solvers import qp
from HeteroskedasticErrors.StatsReader import StatsReader
# Display configurations
#np.set_printoptions(threshold=50)

"""
Main program to solve sequentially (day by day) the portfolio optimization problem of part 2.
"""

## Statistics
print('Reading statistics')

stats = StatsReader('/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/stats/stats.xlsx')
# Dimensionnality of the problem (tickers, days)
m,n = stats.getNumberOfTickers(), stats.getNumberOfDays()

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

#print("Returns:", aritReturns, '\n', logReturns)

# Compute their covariance matrices and annualize them
covLogReturns = np.cov(logReturns)
covAritReturns = np.cov(aritReturns)
annualCovLogReturns = covLogReturns * 252
annualCovAritReturns = covAritReturns * 252

# Compute expected returns and annualize them
expLogReturns = [np.mean(x) for x in logReturns]
expAritReturns = [np.mean(x) for x in aritReturns]
annualExpLogReturns = [(x + 1)**252 - 1 for x in expLogReturns]
annualExpAritReturns = [(x + 1)**252 - 1 for x in expAritReturns]



## Deal with numerical instability in the covariance matrices eigenvalue decompositions.
print('Deal with numerical instability modifying the positive-definite status of the covariance matrix')

# FIRST SOLUTION: Make it closer to the identity matrix by introducing a diagonal constant perturbation.
epsilon = 0.001
annualCovAritReturns += epsilon * np.eye(m)
#print(np.linalg.eigh(annualCovAritReturns))

"""
# SECOND SOLUTION: Keep only the first "Principal Components" of the matrix, removing complex eigenvalues
# Eigenvalue decomposition
eigVal, eigVec = np.linalg.eig(annualCovAritReturns)
eigenvalues = eigVal[:1]
eigenvectorsMatrix = eigVec[:,:1]

# Keep only real eigenvalues
pcCovarianceMatrix = np.zeros((m,m))
for i,x in enumerate(eigenvalues):
    if (x.real == x):
        pcCovarianceMatrix += float(x) * np.outer(np.array(eigenvectorsMatrix[:,i]).astype(float), np.array(eigenvectorsMatrix[:,i]).astype(float))

# Update the covariance matrix
annualCovAritReturns = pcCovarianceMatrix

#print(pcCovarianceMatrix)
#print(np.linalg.eigh(annualCovAritReturns))
"""



## Set the parameters of the problem
print('Initialize parameters of the sequential optimization')

# Lambda, gamma, covariance matrix, expected returns
aversionLambda = 1.
gamma = 1.
P = matrix(-2 * aversionLambda * annualCovAritReturns)
mu = annualExpAritReturns

# Randomly take the initial weights of the portfolio and normalize them
initialWeights = np.random.uniform(low=-1.,high=1.,size = m)
initialWeights = initialWeights / np.linalg.norm(initialWeights)

# Daily weights matrix, daily returns vector and daily risks vector
optWeightSeq = np.zeros((m,n-1))
optWeightSeq[:,0] = initialWeights
riskSeq = np.zeros((1,n-1)).flatten()
retSeq = np.zeros((1,n-1)).flatten()

# Market impact and transaction cost functions (we use Almgren's values)
tempImpact = lambda dayImbalance, dayVolume, sigma, eta=.142, beta=.6 : eta * sigma * pow( abs(dayImbalance) / ((6/6.5) * dayVolume), beta)
permImpact = lambda dayImbalance, dayVolume, sigma, gamma=.314 : gamma * sigma * abs (dayImbalance / dayVolume)
TCperUnit = lambda price, dayImbalance, dayVolume, sigma : price * ( 0.5 * permImpact(dayImbalance, dayVolume, sigma) + tempImpact(dayImbalance, dayVolume, sigma))

## Sequential optimization
## We assume the expected returns and covariance matrices constant over the 64 days
## What changes between each day are the TCVector (i.e. ADVs, imbalances, sigmas)
print('Start daily sequential optimization of the portfolio weights')

# Main loop
for day in range(1,n-1):

    print("Day", day)
    
    # Unit transaction costs for that day
    TCVector = np.array([TCperUnit(VWAPsReshaped[i, day], imbalances[i,day], ADVs[i,day], sigmas[i,day]) for i in range(m)])
    
    # Optimizer matrices
    G = matrix(np.ones((1,m)).flatten() + TCVector).T
    h = matrix(np.ones((1,1)).flatten() + np.dot(initialWeights, TCVector))
    q = matrix(mu - gamma * TCVector)
    A = matrix(np.ones((1,m)).flatten()).T
    b = matrix(np.ones((1,1)).flatten())
    
    #print(np.dot(initialWeights, TCVector),"END")    
    #print(TCVector,"END")
    #print(G,"END")
    #print(h,"END")
    #print(q,"END")
    
    # Optimize with cvxopt quadratic programming function (max(I) = -min(-I)), and get weights
    optWeightSeq[:,day] = -np.array(qp(-P, -q, G, h, A,b, initvals = optWeightSeq[:,day-1])['x']).flatten()
    
    # Compute daily return and risks values
    retSeq[day] = np.dot(mu, optWeightSeq[:,day])
    riskSeq[day] = np.dot(optWeightSeq[:,day], np.dot(annualCovAritReturns, optWeightSeq[:,day]))



## Display results
print("\n End of the simulation",)
print("\n Optimal weights per day (column by column):", optWeightSeq)
