import numpy as np
import scipy.optimize
from HeteroskedasticErrors.StatsReader import StatsReader
# Display configurations
np.set_printoptions(threshold=50)

## FIRST: Compute returns and covariances
# Statistics
print('Reading statistics')
stats = StatsReader('/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/stats/stats.xlsx')
m,n = stats.getNumberOfTickers(), stats.getNumberOfDays()

# Volume weighted average prices (used for returns)
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

## THEN: Create the toy problem. Solve for the mean-variance optimal portfolio before incorporating views.

# Variance + penalty
def fitnessMetric(W, R, C, r):
    # For given level of return r, find weights which minimizes portfolio variance.
    mean_1, var = np.sum(R*W), np.dot(np.dot(W, C), W)
    # Penalty for not meeting stated portfolio return effectively serves as optimization constraint
    # Here, r is the 'target' return
    penalty = 0.1*abs(mean_1-r)
    return var + penalty

# Mean variance optimal portfolio
def markowitzWeights(R, C):
    n = len(R)
    W = np.ones([n])/n # Start with equal weights
    b_ = [(0.1,1) for i in range(n)] # Bounds (decision variables)
    c_ = ({'type':'eq', 'fun': lambda W: np.sum(W)-1. }) # weights must sum to 1 (constraint)
    # 'target' return is the expected return on the market portfolio
    optimized = scipy.optimize.minimize(fitnessMetric, W, (R, C, sum(R*W)), method='SLSQP', constraints=c_, bounds=b_)
    if not optimized.success:
        raise BaseException(optimized.message)
    return optimized.x 

print(annualExpAritReturns, annualCovAritReturns)

# BUG HERE (but functions OK (cf unit test)
# Market portfolio using GLS
marketWeigths = markowitzWeights(annualExpAritReturns, annualCovAritReturns)
mean, var = sum(annualExpAritReturns*marketWeigths), np.dot(np.dot(marketWeigths, annualCovAritReturns), marketWeigths)


## THEN: Incorporate views

# P and Q are the views matrix (for P: a 1 in line is an absolute view, a +1 and -1 is a relative view. Corresponding values in Q vector.)
P = np.identity((m,m))
Q = annualExpAritReturns

# tau is a scalar indicating the uncertainty in the CAPM (Capital Asset Pricing Model) prior
tau = 0.025
# omega represents the uncertainty of our views. Rather than specify the 'confidence'in one's view explicitly, we extrapolate an implied uncertainty from market parameters.
omega = np.dot(np.dot(np.dot(tau, P), annualCovAritReturns), np.transpose(P))

# Compute equilibrium excess returns taking into account views on assets
sub_a = np.linalg.inv(np.dot(tau, annualCovAritReturns))
sub_b = np.dot(np.dot(np.transpose(P), np.linalg.inv(omega)), P)
sub_c = np.dot(np.linalg.inv(np.dot(tau, annualCovAritReturns)), P)
sub_d = np.dot(np.dot(np.transpose(P), np.linalg.inv(omega)), Q)
P_new = np.dot(np.linalg.inv(sub_a + sub_b), (sub_c + sub_d))         

## FINALLY: Perform a mean-variance optimization taking into account views          
new_weights = markowitzWeights(P_new, annualCovAritReturns)

