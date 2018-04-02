from HeteroskedasticErrors.OptimizeEtaBeta import OptimizeEtaBeta
from HeteroskedasticErrors.StatsReader import StatsReader
from HeteroskedasticErrors.GetStdDev import GetStdDev
import numpy as np
np.set_printoptions(threshold=10000000)

'''
Main function to find optimal eta and beta coefficients.
'''

print('Initializing optimizer')
optimizer = OptimizeEtaBeta()

print('Initializing statistics')

# Stats reader
stats = StatsReader('/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/stats/stats.xlsx', boolDisplay=False)
# Temporary impact
h = optimizer.getTempImpact(stats.getVWAPuntil330Vector(), stats.getArrivalPriceVector(), stats.getTerminalPriceVector())
# Sigmas
sigmas = stats.getStdErrorVector()
# Imbalances
imbalances = stats.getImbalanceVector()
# Average daily values
ADVs = stats.getADValuesVector()

print('Retrieving the residuals standard deviations')
stdDevGetter = GetStdDev(h, sigmas, imbalances, ADVs)
# 1st SOLUTION: Try homoskedastic errors
#stdErrs = np.ones(ADVs.shape)
# 2nd SOLUTION: Back-out Lambdas vector in one step using Almgren's values
#stdErrs = stdDevGetter.getLambdasVectorOneStep()
# 3rd SOLUTION: Back-out Lambdas vector in one step (homosked->(eta,beta)->lambda_is from there
stdErrs = stdDevGetter.getLambdasVectorOneStepHomo()

print(stdErrs)

print('Computing optimal eta and beta')
# Vector eta, beta
res = optimizer.getOptimalEtaBeta(h, sigmas, imbalances, ADVs, np.ones(ADVs.shape))
        
print(res)