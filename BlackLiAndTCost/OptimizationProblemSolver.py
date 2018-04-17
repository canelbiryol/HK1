import numpy as np
from cvxopt import matrix
from cvxopt.solvers import qp
from HeteroskedasticErrors.StatsReader import StatsReader
# Display configurations
np.set_printoptions(threshold=50)

# Statistics
print('Reading statistics')
stats = StatsReader('/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/stats/stats.xlsx')
m,n = stats.getNumberOfTickers(), stats.getNumberOfDays()

# Sigmas
sigmas = stats.getStdErrorVector().reshape(m,n-1)
# Imbalances
imbalances = stats.getImbalanceVector().reshape(m,n-1)
# Average daily values
ADVs = stats.getADValuesVector().reshape(m,n-1)
# Volume weighted average prices
VWAPs = stats.getVWAPuntil400Vector()

# Get daily returns from VWAP and reshape them into a numpy matrix
print('Computing returns and covariances')
aritReturns = np.empty((1, stats.getNumberOfTickers() * (stats.getNumberOfDays() - 1))).flatten()
logReturns = np.empty((1, stats.getNumberOfTickers() * (stats.getNumberOfDays() - 1))).flatten()
f_aritR = lambda ri, rf: (rf - ri) / ri
aritReturns[1:] = np.asarray([f_aritR(VWAPs[i], rf) for i,rf in enumerate(VWAPs[1:])])
logReturns[1:] = np.diff(np.log(VWAPs))
# dummy first return to be able to reshape into a matrix
aritReturns[0] = logReturns[1]
logReturns[0] = logReturns[1]
aritReturns = np.reshape(aritReturns, (stats.getNumberOfTickers(), stats.getNumberOfDays() - 1))
logReturns = np.reshape(logReturns, (stats.getNumberOfTickers(), stats.getNumberOfDays() - 1))
#print(aritReturns, '\n', logReturns)

# Compute their covariance matrix
covLogReturns = np.cov(logReturns)
covAritReturns = np.cov(aritReturns)

# And expected returns
expLogReturns = [np.mean(x) for x in aritReturns]
expAritReturns = [np.mean(x) for x in logReturns]

# Annualize everything
annualCovLogReturns = covLogReturns * 252
annualCovAritReturns = covAritReturns * 252
annualExpLogReturns = [(x + 1)**252 - 1 for x in expLogReturns]
annualExpAritReturns = [(x + 1)**252 - 1 for x in expAritReturns]

# Define the market impact function
TC = lambda dayImbalance, dayVolume, sigma, eta=.142, beta=.6 : eta * sigma * pow( abs(dayImbalance) / ((6/6.5) * dayVolume), beta)

# Optimize with cvxopt (using max(I) = -min(-I))
print('Start the sequential optimization')
aversionLambda = 1.
gamma = 1.
P = matrix(-aversionLambda * annualCovAritReturns)
mu = annualExpAritReturns
initialWeights = np.random.uniform(low=-1.,high=1.,size = m)
initialWeights = initialWeights / np.linalg.norm(initialWeights)

# Daily weights, returns and risks
optWeightSeq = np.zeros((m,n-1))
optWeightSeq[:,0] = initialWeights
riskSeq = np.zeros((1,n-1))
retSeq = np.zeros((1,n-1))

# BUG HERE
#TODO Uncomment when debugged and remove dummy loop
# for day in range(1,n):
for day in range(1,2):
    print(day)
    TCVector = np.array([TC(imbalances[i,day], ADVs[i,day], sigmas[i,day]) for i in range(m)])
    G = matrix(np.ones((1,m)).flatten() + TCVector).T
    h = matrix(np.ones((1,1)).flatten() + np.dot(initialWeights, TCVector))
    q = matrix(mu - gamma * TCVector)

    #print(np.dot(initialWeights, TCVector))    
    #print(TCVector)
    #print(G)
    #print(h)
    #print(q)

    optWeightSeq[day,:] = - qp(-P, -q, G, h, initvals = optWeightSeq[:,day-1])['x']
    retSeq[day] = np.dot(mu, optWeightSeq[day,:])
    riskSeq[day] = np.dot(optWeightSeq[day,:], np.dot(annualCovAritReturns, optWeightSeq[day,:]))
