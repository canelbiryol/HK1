from HeteroskedasticErrors.OptimizeEtaBeta import OptimizeEtaBeta
from HeteroskedasticErrors.StatsReader import StatsReader
from HeteroskedasticErrors.GetStdDev import GetStdDev
from scipy import stats as st
import matplotlib.pyplot as plt
import numpy as np
from HeteroskedasticErrors.WhiteTestHomoskedasticity import WhiteTestHomoskedasticity

# Display configurations
np.set_printoptions(threshold=50)

'''
Main function to find optimal eta and beta coefficients.
'''

""" Initialize stats """
print('Initializing optimizer and statistics')
optimizer = OptimizeEtaBeta()
stats = StatsReader('/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/stats/stats.xlsx')

# Temporary impact
h = optimizer.getTempImpact(stats.getVWAPuntil330Vector(), stats.getArrivalPriceVector(), stats.getTerminalPriceVector())
# Sigmas
sigmas = stats.getStdErrorVector()
# Imbalances
imbalances = stats.getImbalanceVector()
# Average daily values
ADVs = stats.getADValuesVector()

""" Get standard deviation of residuals """
print('Retrieving the residuals\' standard deviations')
stdDevGetter = GetStdDev(h, sigmas, imbalances, ADVs)
# 1st SOLUTION: Try homoskedastic errors
#stdErrs = np.ones(ADVs.shape)
# 2nd SOLUTION: Back-out Lambdas vector in one step using Almgren's values
#stdErrs = stdDevGetter.getLambdasVectorOneStep()
# 3rd SOLUTION: Back-out Lambdas vector in one step (homosked->(eta,beta)->lambda_is from there
stdErrs = stdDevGetter.getLambdasVectorOneStepHomo()

""" Compute optimal eta and beta """
print('Computing optimal eta and beta')
res = optimizer.getOptimalEtaBeta(h, sigmas, imbalances, ADVs, np.ones(ADVs.shape))
print('Values of eta and beta:', res.x)
tStats = optimizer.getTstatsEtaBeta(res.x, sigmas, imbalances, ADVs, stdErrs)
print('t-statistics of eta and beta:', tStats)

""" Analyze residuals """
print('Analyzing standardized residuals')
residuals = (h - res.x[0] * sigmas * pow( np.abs(imbalances)/(ADVs * (6/6.5)) , res.x[1]))/stdErrs
residualAnalysis = st.describe(residuals)
print('Residuals statistics:', residualAnalysis)
# Histogram
print('Plot residuals\' histogram after removing outliers (+/- 5 standard deviations')
reject_outliers = lambda data, m: data[abs(data - np.mean(data)) < m * np.std(data)]
residualsCleaned = reject_outliers(residuals,4)
plt.hist(residualsCleaned)
print("Please close the plot to continue")
#plt.show()
plt.savefig("residuals.png")

""" Analysis of residuals for hetero/homos-skedasticity """
print('Analyzing standardized residuals')
wTest = WhiteTestHomoskedasticity(residuals, stats.getNumberOfTickers())
# Reject homoskedasticity if p is very small
print("p-value of White's test is (small means heteroskedastic, as expected):", wTest.getPValue())


""" Analyze optimal eta and beta for active and passive stocks """ 
## ACTIVE
print('Initialize statistics of active stocks for analysis')
statsActiveStocks = StatsReader('/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/stats/stats.xlsx', actPass=[True,False])
# Temporary impact
hAct = optimizer.getTempImpact(statsActiveStocks.getVWAPuntil330Vector(), statsActiveStocks.getArrivalPriceVector(), statsActiveStocks.getTerminalPriceVector())
# Sigmas
sigmasAct = statsActiveStocks.getStdErrorVector()
# Imbalances
imbalancesAct = statsActiveStocks.getImbalanceVector()
# Average daily values
ADVsAct = statsActiveStocks.getADValuesVector()
# Std of residuals
stdDevGetterAct = GetStdDev(hAct, sigmasAct, imbalancesAct, ADVsAct)
stdErrsAct = stdDevGetterAct.getLambdasVectorOneStepHomo()
# Optimal eta and beta
print('Computing optimal eta and beta active stocks')
resAct = optimizer.getOptimalEtaBeta(hAct, sigmasAct, imbalancesAct, ADVsAct, np.ones(ADVsAct.shape))
print('Values of eta and beta active stocks:', resAct.x)
tStatsAct = optimizer.getTstatsEtaBeta(resAct.x, sigmasAct, imbalancesAct, ADVsAct, stdErrsAct)
print('t-statistics of eta and beta active stocks:', tStatsAct)

## PASSIVE
print('Initialize statistics of passive stocks for analysis')
statsPassiveStocks = StatsReader('/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/stats/stats.xlsx', actPass=[False,True])
# Temporary impact
hPas = optimizer.getTempImpact(statsPassiveStocks.getVWAPuntil330Vector(), statsPassiveStocks.getArrivalPriceVector(), statsPassiveStocks.getTerminalPriceVector())
# Sigmas
sigmasPas = statsPassiveStocks.getStdErrorVector()
# Imbalances
imbalancesPas = statsPassiveStocks.getImbalanceVector()
# Average daily values
ADVsPas = statsPassiveStocks.getADValuesVector()
# Std of residuals
stdDevGetterPas = GetStdDev(hPas, sigmasPas, imbalancesPas, ADVsPas)
stdErrsPas = stdDevGetterPas.getLambdasVectorOneStepHomo()
# Optimal eta and beta
print('Computing optimal eta and beta passive stocks')
resPas = optimizer.getOptimalEtaBeta(hPas, sigmasPas, imbalancesPas, ADVsPas, np.ones(ADVsPas.shape))
print('Values of eta and beta passive stocks:', resPas.x)
tStatsPas = optimizer.getTstatsEtaBeta(resPas.x, sigmasPas, imbalancesPas, ADVsPas, stdErrsPas)
print('t-statistics of eta and beta passive stocks:', tStatsPas)
