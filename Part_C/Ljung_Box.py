'''
Created on Mar 3, 2018
@author: Michael
'''
import numpy as np
from scipy.stats import chi2

class Ljung_Box(object):
    '''
    Class to perform Ljung-Box test
    '''
    def __init__(self, dataSet):
        '''
        Stores the data set inside the class to perform the analysis
        '''
        self.dataSet = np.asarray(dataSet)    
    
    def changeDataSet(self, newDataSet):
        '''
        Allows the user to change the data set
        '''
        self.dataSet = np.asanyarray(newDataSet)
        
    def inspectDataSet(self):
        '''
        Returns the data set
        '''
        return self.dataSet    
    
        
    def getQuantile(self, lagNumber ):
        '''
        Returns the quantile of the chi-squared distribution of the test statistic
        '''
        if (lagNumber>(len(self.dataSet)-2)):
            raise Exception('Lag number must be at least 2 units smaller than the length of the data set.')
        
        N = len(self.dataSet)
        Q = 0
        for x in range(1,lagNumber+1,1):
            length = len(self.dataSet)
            S = np.corrcoef(self.dataSet[x:length],self.dataSet[0:-x])[1,0]
            Q += S*S/(N-x)
        
        Q *= N*(N+2)
        
        quantile = chi2.cdf(Q, lagNumber)
        print("The Ljung-Box test statistic for lag number", lagNumber,"is", quantile,".")     
        
        return quantile
    
    
    def getAutocorrelation(self, lagNumber):
        length = len(self.dataSet)
        return np.corrcoef(self.dataSet[lagNumber:length],self.dataSet[0:-lagNumber])[1,0]
    