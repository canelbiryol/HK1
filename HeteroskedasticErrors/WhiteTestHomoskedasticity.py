import numpy as np
from scipy.stats import chi2

class WhiteTestHomoskedasticity(object):
    '''
    We try: 
        H0: residuals^2 = delta_0 for ticker A; residuals^2 = delta_1 for ticker B ... (heteroskedastic)
        against
        H1: residuals^2 = delta for all stocks (homoskedastic)
        
    In each case, the best deltas are the arithmetic mean of the samples (empirical variances since the residuals are centered)
    
    To call with: residuals - residuals of the regression of temp impact against ...
                  degreesOfFreedom - stats.getNumberOfTickers
    '''

    def __init__(self, residuals, degreesOfFreedom):

        # Check for consistency
        if (len(residuals) % degreesOfFreedom != 0):
            raise Exception( 'Residuals should be the vector of residuals stacked by category.' )

        self._df = degreesOfFreedom
        self._numberOfObservation = int(len(residuals) / degreesOfFreedom)
        self._residualsSquared = np.power(residuals, 2)
        self._residualsSquaredBar = np.mean(self._residualsSquared)
        
        # Fit the model
        self._residualsHomo = self._residualsSquaredBar * np.ones_like(self._residualsSquared)
        self._residualsHetero = np.array([np.mean(self._residualsSquared[i * self._numberOfObservation : (i+1) * self._numberOfObservation]) * np.ones(self._numberOfObservation) for i in range(0, self._df)]).flatten()
        
    def getTSS(self):
        return(np.sum(pow((self._residualsHomo - self._residualsSquared),2)))
    
    def getRegSS(self):
        return(np.sum(pow((self._residualsHetero - self._residualsSquared),2)))
    
    def getRSquared(self):
        return(1 - self.getRegSS()/self.getTSS())
    
    def getPValue(self):
        return(chi2.pdf(self._numberOfObservation * self.getRSquared(), self._df - 1))
    