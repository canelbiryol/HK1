'''
Created on Mar 3, 2018
@author: Michael
'''
from statsmodels.tsa.stattools import adfuller

def stationaryTest(data, windowSize):
    '''We perform the ADF based on what the data looks like'''
    '''Unit root with time trend does not make sense. Need to decide between drift and no drift.'''
    '''Number of lags will be based on where we observe the autocorrelation to be very close to 0.'''
    #http://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.adfuller.html
    result = adfuller(data, maxlag=None, regression='c', autolag='AIC', store=False, regresults=False)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))