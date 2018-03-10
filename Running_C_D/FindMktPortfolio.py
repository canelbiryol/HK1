'''
Created on Mar 9, 2018

@author: Michael
'''
import numpy as np
import pandas as pd
from adjustAndClean.TAQAdjust import TAQAdjust
from adjustAndClean.TAQCleaner import TAQCleaner
from adjustAndClean.StackData import StackData
from partB.xMinuteReturn import getXSecMidQuoteReturns
from math import sqrt
from cvxopt import matrix
from cvxopt.blas import dot
from cvxopt.solvers import qp, options

print('Initializing.')

    # FIRST: Take S&P500 tickers
s_p500 = '/Users/Michael/eclipse-workspace/Homework_1/s_p500.xlsx'
s_p500xls = pd.read_excel(open(s_p500,'rb'), sheet_name='WRDS')
s_ptickers = np.unique((np.array(s_p500xls['Ticker Symbol'])).astype(str))
s_ptickers = s_ptickers[:-1]

baseDir = '/Users/Michael/Documents/TAQ/R'
startDate = '20070620'
endDate = '20070721'
tickers = []
tickers.append('AAPL')
tickers.append('MSFT')
tickers.append('AMZN')
tickers.append('JPM')
tickers.append('JNJ')
tickers.append('GOOG')
tickers.append('XOM')
tickers.append('BAC')
tickers.append('WFC')
tickers.append('INTC')

print(tickers[0])
print(type(tickers[0]))

returns = np.zeros((11,409))

for k in range(10):
    # Stack everything
    ticker = tickers[k]
    stack = StackData(baseDir, startDate, endDate, ticker)
    stack.addTrades()
    stack.addQuotes()
    print('Finished stacking')
    # Get results
    quotes = stack.getStackedQuotes()
    trades = stack.getStackedTrades()
    print('Got results')         
    # Adjust
    adjuster = TAQAdjust( quotes, trades, s_p500 )
    adjuster.adjustQuote()
    print('Adjusted')
    # Clean
    cleaner = TAQCleaner(quotes, trades)
    quotes = np.delete(quotes, cleaner.cleanQuotesIndices(), axis = 0)
    print('Cleaned')
    q_returns = getXSecMidQuoteReturns(quotes,900)[0]
    for x in range(len(q_returns)):
        returns[k,x] = q_returns[x]
    print('length of', tickers[k],' is',len(q_returns))
    
MeanVector = np.zeros(11)


for x in range(409):
    returns[10,x] = 1
    # dummy variable used for covariance
#Convert to annualized
for x in range(10):
    print(np.mean(returns[x,:]))
    MeanVector[x] = ((np.mean(returns[x,:])+1)**(26*252))-1

MeanVector[10] = 0.0378
Covariance = np.cov(returns)*26*252
print(MeanVector)
print(Covariance)

#Feed into cvxopt
n = 11
S = matrix( Covariance )
pbar = matrix(MeanVector)

G = matrix(0.0, (n,n))
G[::n+1] = -1.0
h = matrix(0.0, (n,1))
A = matrix(1.0, (1,n))
b = matrix(1.0)

N = 1000
mus = [ 10**(5.0*t/N-1.0) for t in range(N) ]
options['show_progress'] = False
xs = [ qp(mu*S, -pbar, G, h, A, b)['x'] for mu in mus ]
returns = [ dot(pbar,x) for x in xs ]
risks = [ sqrt(dot(x, S*x)) for x in xs ]

try: import pylab
except ImportError: pass
else:
    pylab.figure(1, facecolor='w')
    pylab.plot(risks, returns)
    pylab.xlabel('standard deviation')
    pylab.ylabel('expected return')
    pylab.axis([0, 0.2, 0, 0.15])
    pylab.title('Risk-return trade-off curve (fig 4.12)')
    pylab.yticks([0.00, 0.05, 0.10, 0.15])
    pylab.show()

risk_free = returns[0]
best_sharpe = 0
best_sharpe_index = 0
for x in range(len(returns)):
    if ((returns[x]-risk_free)/risks[x])>best_sharpe:
        best_sharpe = (returns[x]-risk_free)/risks[x]
        best_sharpe_index = x

print('Optimal portfolio returns:', returns[best_sharpe_index])
print('Optimal portfolio std dev:',risks[best_sharpe_index])
print('Optimal portfolio weights:')
print(xs[best_sharpe_index])


