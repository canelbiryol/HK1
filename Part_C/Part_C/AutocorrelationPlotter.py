'''
Created on Mar 6, 2018

@author: Michael
'''
import numpy as np
from Part_C.Ljung_Box import Ljung_Box
import matplotlib.pyplot as plt

def plotAutocorrelation(data, n_lags, windowSize):
    
    Plotter = Ljung_Box(data)
    X = np.arange(1,n_lags+1,1)
    Y = np.zeros(n_lags)
    
    for x in range(n_lags):
        Y[x] = Plotter.getAutocorrelation(int(x+1))
    
    plt.clf()
    plt.plot(X,Y)
    plt.xlabel('Lag Number')
    plt.ylabel('Autocorrelation')
    plt.title('Autocorrelation with window size of %i seconds' %windowSize)
    plt.show()