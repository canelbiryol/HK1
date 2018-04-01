from HeteroskedasticErrors.OptimizeEtaBeta import getOptimalEtaBeta, getTempImpact
from HeteroskedasticErrors.StatsReader import StatsReader
from HeteroskedasticErrors.GetStdDev import GetStdDev

'''
TODO: WRITE SPEC
'''

print('Initializing.')

# Stats reader
stats = StatsReader('/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/stats/stats.xlsx', boolDisplay=True)
# Temporary impact
h = getTempImpact(stats.getVWAPuntil330Vector(), stats.getArrivalPriceVector(), stats.getTerminalPriceVector())
# Sigmas
sigmas = stats.getStdErrorVector()
# Imbalances
imbalances = stats.getImbalanceVector()
# Average daily volume
ADVs = stats.getADVVector()

# Lambda_is backed-out using Almgren's values
StdErrs = GetStdDev(h, sigmas, imbalances, ADVs)

# Vector eta, beta
res = getOptimalEtaBeta(h, sigmas, imbalances, ADVs, StdErrs)