from HeteroskedasticErrors.OptimizeEtaBeta import OptimizeEtaBeta
from HeteroskedasticErrors.StatsReader import StatsReader
from HeteroskedasticErrors.GetStdDev import GetStdDev

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
# Lambda_is backed-out using Almgren's values
StdErrs = GetStdDev(h, sigmas, imbalances, ADVs).getLambdasVector()

print('Computing optimal eta and beta')
# Vector eta, beta
res = optimizer.getOptimalEtaBeta(h, sigmas, imbalances, ADVs, StdErrs)
        
print(res)