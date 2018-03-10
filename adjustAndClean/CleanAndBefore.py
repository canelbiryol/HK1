from matplotlib import pyplot as plt
from adjustAndClean.StackData import StackData
from adjustAndClean.TAQAdjust import TAQAdjust
from adjustAndClean.TAQCleaner import TAQCleaner
from copy import deepcopy
import numpy as np

def plotSeries(series1, series2, index_price, ticker, title, outputFile):
    fig = plt.figure()
    
    lblQ = ticker + ' before'
    lblT = ticker + ' after'
    
    plt.plot(series1[:,index_price].astype(float), label = lblQ)
    plt.plot(series2[:,index_price].astype(float), label = lblT) 

    plt.gcf().autofmt_xdate()
    plt.title(title)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper right", borderaxespad=0.)
    plt.show(block=False)
    
    fig.savefig(outputFile)
    print("plot successful")


def plotCleanAndBefore(s_p500, baseDir, filePathcln, ticker):
    # Stack
    stack = StackData(baseDir, '20070625', '20070629', ticker)
    stack.addQuotes()
    stack.addTrades()
    print('Finished stacking', ticker)

    # Get stacked results
    quotes = stack.getStackedQuotes()
    trades = stack.getStackedTrades()
    print('Got stacked results', ticker)

    # Adjustment
    adjuster = TAQAdjust( quotes, trades, s_p500 )
    adjuster.adjustQuote()
    adjuster.adjustTrade()
    quotesbefore = deepcopy(quotes)
    tradesbefore = deepcopy(trades)
    print('Finished adjustment', ticker)

    # Cleaning
    cleaner = TAQCleaner( quotes, trades )
    quotes = np.delete(quotes, cleaner.cleanQuotesIndices(), axis = 0)
    trades = np.delete(trades, cleaner.cleanTradesIndices(), axis = 0)
    print('Finished cleaning', ticker)

    # Plot quotes
    title = ticker + ' quotes before and after cleaning'
    outputFile = filePathcln + ticker + "quotes_cleaning.png"
    plotSeries(quotes, quotesbefore, 3, ticker, title, outputFile)

    # Plot trades
    title = ticker + ' trades before and after cleaning'
    outputFile = filePathcln + ticker + "trades_cleaning.png"
    plotSeries(trades, tradesbefore, 3, ticker, title, outputFile)
    
if __name__ == '__main__':
    s_p500 = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/s_p500.xlsx'
    baseDir = '/media/louis/DATA/Courant_dataset_matlab/R'
    filepathcln = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/plots/'
    ticker = 'MSFT'
    plotCleanAndBefore(s_p500, baseDir, filepathcln, ticker)
