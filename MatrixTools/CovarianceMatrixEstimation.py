from HeteroskedasticErrors.StatsReader import StatsReader
import json
from numpy import  floor
import numpy as np
from MatrixTools.PreparePredictors import PreparePredictors
from MatrixTools.CovarianceMatrices import CovarianceCalculator
from MatrixTools.CheckVolatility import CheckVolatility, getWeights
from MatrixTools.ExtraCreditCovariance import ExtraCreditCovariance

def flatten(lst):
    i=0
    while i<len(lst):
        while True:
            try:
                lst[i:i+1] = lst[i]
            except (TypeError, IndexError):
                break
        i += 1

stats = StatsReader(statsPath='/Users/canelbiryol/Data/new_stats/stats.xlsx', boolDisplay=False, actPass=[False,False], flatten=True)

returns = stats.get2minRetArraysVector()
train_index = 45

values = {}

trainingData = []
testingData = []

for i in range(0, len(returns), 65):
    train = []
    test = []
    
    for j in range(65):
        arr = eval(returns[i+j])
        # arr = np.array(arr, dtype=np.float)
        arr = [0.0 if v is None else v for v in arr]
        if j < train_index:
            train += arr
        else:
            test += arr

    trainingData.append(train)
    testingData.append(test)

trainingData = np.array(trainingData)
testingData = np.array(testingData)

P = PreparePredictors(testingData)
p_minVar = P.getMinVarPredictor() # minimum variance predictor
p_omni = P.getOmniscientPredictor() # omniscent predictor
p_random = P.getRandomPredictor() # random predictor

C = CovarianceCalculator(trainingData)
c_emp = C.getEmpiricalCovariance() # empirical covariance
c_clipped = C.getClippedCovariance() # clipped covariance
c_LW = C.getLedoitWolfCovariance() # Ledoit-Wolf covariance

C_ec = ExtraCreditCovariance(trainingData)
c_extra = C_ec.getCovariance() # Dispersion Bias covariance

covarianceMatrices = [c_emp, c_clipped, c_LW, c_extra]
             
V = CheckVolatility(testingData)

minVar = []    
for c in covarianceMatrices:
        minVar.append(V.checkVolatility(c, p_minVar))

omni = []
for c in covarianceMatrices:
        omni.append(V.checkVolatility(c, p_omni))
        
rand = []
for c in covarianceMatrices:
        rand.append(V.checkVolatility(c, p_random))
        
print("---------------------------")
print("Minimum Variance Portfolio")
print("---------------------------")
print("Empirical: " + str(minVar[0]))
print("Clipped: " + str(minVar[1]))
print("Ledoit Wolf: " +  str(minVar[2]))
print("Dispersion Bias: "  + str(minVar[3]))

print("---------------------------")
print("Omniscent Predictor")
print("---------------------------")
print("Empirical: " + str(omni[0]))
print("Clipped: " + str(omni[1]))
print("Ledoit Wolf: " + str(omni[2]))
print("Dispersion Bias: "  + str(omni[3]))

print("---------------------------")
print("Random Predictor")
print("---------------------------")
print("Empirical: " + str(rand[0]))
print("Clipped: " + str(rand[1]))
print("Ledoit Wolf: "  + str(rand[2]))
print("Dispersion Bias: "  + str(rand[3]))
        

