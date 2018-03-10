'''
Created on Mar 7, 2018

@author: Michael
'''
import numpy as np
import pandas as pd
from adjustAndClean.TAQAdjust import TAQAdjust
from adjustAndClean.TAQCleaner import TAQCleaner
from adjustAndClean.StackData import StackData
from partB.xMinuteReturn import getXSecMidQuoteReturns
from partB.xMinuteReturn import getXSecTradeReturns
from Part_C.AutocorrelationPlotter import plotAutocorrelation
from Part_C.Ljung_Box import Ljung_Box
from statsmodels.tsa.stattools import adfuller

print('Initializing.')

    # FIRST: Take S&P500 tickers
s_p500 = '/Users/Michael/eclipse-workspace/Homework_1/s_p500.xlsx'
s_p500xls = pd.read_excel(open(s_p500,'rb'), sheet_name='WRDS')
s_ptickers = np.unique((np.array(s_p500xls['Ticker Symbol'])).astype(str))
s_ptickers = s_ptickers[:-1]

baseDir = '/Users/Michael/Documents/TAQ/R'
startDate = '20070620'
endDate = '20070921'
ticker = 'MSFT'

# Stack everything
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
adjuster.adjustTrade()
print('Adjusted')
            
# Clean
cleaner = TAQCleaner(quotes, trades)
quotes = np.delete(quotes, cleaner.cleanQuotesIndices(), axis = 0)
trades = np.delete(trades, cleaner.cleanTradesIndices(), axis = 0)
print('Cleaned')

'''
plotWindows = np.array([10, 30, 60, 300, 600, 900, 1800])
for x in range(len(plotWindows)):
    t_returns = getXSecTradeReturns(trades,plotWindows[x])[0]
    plotAutocorrelation(t_returns, 50, plotWindows[x])
'''

    
'''At this point, look at the data, the autocorrelation should drop off at around lag K=5?'''
K=5
confidence = 0.95

testWindows = 60*np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])
quantiles = np.zeros(len(testWindows))
for x in range(len(testWindows)):
    t_returns = getXSecTradeReturns(trades,testWindows[x])[0]
    print(len(t_returns))
    LB_t = Ljung_Box(t_returns)
    quantiles[x] = LB_t.getQuantile(K)
    print('Quantile for',testWindows[x],'second trades is',quantiles[x])



#Read the quantiles. Pick the smallest window size such that the quantile>0.95

optimal_Window = -1
for x in range(len(testWindows)):
    if quantiles[x]>confidence:
        continue
    else:
        optimal_Window = testWindows[x]
        break


print('Using window of',optimal_Window,'seconds.')
if optimal_Window == -1:
    print('Error! Make larger test windows.')

t_returns = getXSecTradeReturns(trades,optimal_Window)[0]
q_returns = getXSecMidQuoteReturns(quotes,optimal_Window)[0]

result = adfuller(t_returns, maxlag=5, regression='c', autolag='AIC', store=False, regresults=False)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))

result = adfuller(q_returns, maxlag=5, regression='c', autolag='AIC', store=False, regresults=False)
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))       
   
