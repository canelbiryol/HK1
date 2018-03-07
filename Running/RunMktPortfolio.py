'''
Created on Mar 7, 2018

@author: Michael
'''
import numpy as np
import pandas as pd
from adjustAndClean.TAQAdjust import TAQAdjust
from adjustAndClean.TAQCleaner import TAQCleaner
from adjustAndClean.StackData import StackData
from partB.xMinuteReturn import getXMinuteMidQuoteReturns

from math import sqrt
from cvxopt import matrix
from cvxopt.blas import dot
from cvxopt.solvers import qp
import pylab



s_p500 = '/Users/Michael/eclipse-workspace/Homework_1/s_p500.xlsx'
s_p500xls = pd.read_excel(open(s_p500,'rb'), sheet_name='WRDS')
s_ptickers = np.unique((np.array(s_p500xls['Ticker Symbol'])).astype(str))
s_ptickers = s_ptickers[:-1]
       
baseDir = '/Users/Michael/Documents/TAQ/R'
startDate = '20070620'
endDate = '20070920'
windowSize = 3600
r = 0.00002448
'''Replace this with the windowSize determined in LjungBox'''

N = len(s_ptickers)
SPXreturns = np.zeros(N+1)

counter = 0
# THEN: Loop through tickers and stack them separately
for ticker in s_ptickers:
            
    # Stack everything
    stack = StackData(baseDir, startDate, endDate, ticker)
    stack.addTrades()
    stack.addQuotes()
            
    # Get results
    quotes = stack.getStackedQuotes()
    trades = stack.getStackedTrades()
            
    # Adjust
    adjuster = TAQAdjust( quotes, trades, ticker, s_p500 )
    adjuster.adjustQuote()
    adjuster.adjustTrade()
            
    # Clean
    cleaner = TAQCleaner(quotes, trades)
    quotes = np.delete(quotes, cleaner.cleanQuotesIndices(), axis = 0)
    trades = np.delete(trades, cleaner.cleanTradesIndices(), axis = 0)
    
    SPXreturns[counter] = getXMinuteMidQuoteReturns(quotes, windowSize)
    counter += 1.
    
'''Added a cash asset'''
SPXreturns[N] = r*np.ones(len(SPXreturns[0]))

MeanVector = np.zeros(N+1)
for x in range(N+1):
    MeanVector[x] = np.mean(SPXreturns[x])
CovarianceMatrix = np.cov(SPXreturns)


# Problem data.
n = N
S = matrix(CovarianceMatrix)
pbar = matrix(MeanVector)
G = matrix(0.0, (n,n))
G[::n+1] = -1.0
h = matrix(0.0, (n,1))
A = matrix(1.0, (1,n))
b = matrix(1.0)

# Compute trade-off.
M = 100
mus = [ 10**(5.0*t/M-1.0) for t in range(N) ]
portfolios = [ qp(mu*S, -pbar, G, h, A, b)['x'] for mu in mus ]
returns = [ dot(pbar,x) for x in portfolios ]
risks = [ sqrt(dot(x, S*x)) for x in portfolios ]

risk_free = r
sharpe = 0
index = -1
for x in range(len(portfolios)):
    new_sharpe = (returns[x]-risk_free)/risks[x]
    if new_sharpe>sharpe:
        sharpe = new_sharpe
        index = x
        
optimal_portfolio = portfolios[x]

for x in range(len(optimal_portfolio)-1):
    print(s_ptickers[x],'has weight', optimal_portfolio[x],'.',)
print('Cash has weight', optimal_portfolio[len(optimal_portfolio)])     