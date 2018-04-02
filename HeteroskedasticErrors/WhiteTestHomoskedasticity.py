import numpy as np
from scipy.stats import chi2
from scipy.optimize import minimize

class WhiteTestHomoskedasticity(object):
    '''
    TODO: Write Spec
    
    FOR EXPLANATION, SEE SLIDE 9 OF: http://www.fsb.miamioh.edu/evenwe/courses/eco311/sp2017/notes/ch8_notes.pptx
    
    To call with: y - fitted temporary impact of the main regression
                  residuals - residuals of the regression of temp impact against ...
                  degreesOfFreedom - stats.getNumberOfDays() (or stats.getNumberOfTickers ??)
    TODO: Test (Test_WhiteTest)
    '''

    def __init__(self, y, residuals, degreesOfFreedom):

        # Check for consistency
        self._N = len(residuals)
        if (len(residuals)!=self._N or len(y)!=self._N):
            raise Exception( 'All parameters should have the same length.' )

        self._y = y
        self._df = degreesOfFreedom
        self._residuals = residuals
        self._residualsbar = np.sum(residuals)/len(residuals)
        
        # Fit the model
        self._alpha, self._gamma = self.fitWhiteRegression().x[0], self.fitWhiteRegression().x[1]
        self._fittedResiduals = self._alpha * self._y + self._gamma * np.power(self._y,2)

    def RSS(self, X, residuals, y):
        
        alpha = X[0]
        gamma = X[1]

        RSS = 0
        for i in range(self._N):
            RSS += pow(pow(residuals[i],2) - alpha * y[i] - gamma * pow(y[i],2),2)

        return RSS
    
    def fitWhiteRegression(self, alpha0=1., gamma0=1.):

        startPoint = np.array([alpha0, gamma0])
        optiResult = minimize(fun=self.RSS, x0=startPoint, args=(self._residuals, self._y), method='BFGS', options={'disp': True})
        
        # alpha and gamma, as well as optimizing info
        return(optiResult)

    def getTSS(self):
        return(np.sum(pow((self._residuals - self._residualsbar),2)))
    
    def getRegSS(self):
        return(np.sum(pow((self._fittedResiduals - self._residualsbar),2)))
    
    def getRSquared(self):
        return(self.getRegSS()/self.getTSS())
    
    def getPValue(self):
        return(chi2.pdf(self._df * self.getRSquared(), self._df))
    
    def getCoefficients(self):
        return(np.array([self._alpha, self._gamma]))
    
    