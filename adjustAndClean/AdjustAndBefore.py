from matplotlib import pyplot as plt
from adjustAndClean.StackData import StackData
from adjustAndClean.TAQAdjust import TAQAdjust
from adjustAndClean.AdjustingHashmap import AdjustingHashmap
from copy import deepcopy

def plotSeries(series1, series2, index_price, ticker, title, outputFile):
    fig = plt.figure()
    
    lblQ = ticker + ' after'
    lblT = ticker + ' before'
    
    plt.plot(series1[:,index_price].astype(float), label = lblQ)
    plt.plot(series2[:,index_price].astype(float), label = lblT) 

    plt.gcf().autofmt_xdate()
    plt.title(title)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper right", borderaxespad=0.)
    plt.show(block=False)
    
    fig.savefig(outputFile)
    plt.close(fig)
    print("plot successful")


def plotAdjustAndBefore(s_p500, baseDir, filePathcadj, ticker):
    # Multipliers map
    multmap = AdjustingHashmap(s_p500)
    print('Finished building multipliers map', ticker)
    
    # Stack
    stack = StackData(baseDir, '20070625', '20070629', ticker)
    stack.addQuotes()
    stack.addTrades()
    print('Finished stacking', ticker)

    # Get stacked results
    quotes = stack.getStackedQuotes()
    trades = stack.getStackedTrades()
    quotesbefore = deepcopy(quotes)
    tradesbefore = deepcopy(trades)
    print('Got stacked results', ticker)

    # Adjust
    adjuster = TAQAdjust( quotes, trades, ticker, multmap )
    adjuster.adjustQuote()
    adjuster.adjustTrade()
    print('Finished adjustment', ticker)

    # Plot trades
    title = ticker + ' trades before and after adjustment'
    outputFile = filePathcadj + ticker + "trades_adjustment.png"
    plotSeries(trades, tradesbefore, 3, ticker, title, outputFile)

    # Plot quotes
    title = ticker + ' quotes before and after adjustment'
    outputFile = filePathcadj + ticker + "quotes_adjustment.png"
    plotSeries(quotes, quotesbefore, 3, ticker, title, outputFile)
    
if __name__ == '__main__':
    s_p500 = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/s_p500.xlsx'
    baseDir = '/media/louis/DATA/Courant_dataset_matlab/R'
    filepathadj = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/plots/'
    ticker = 'GOOG'
    plotAdjustAndBefore(s_p500, baseDir, filepathadj, ticker)
