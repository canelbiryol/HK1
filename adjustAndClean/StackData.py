from impactModel.FileManager import FileManager
import numpy as np

class StackData(object):
    '''
    Class compiling the data on one ticker into two arrays.
    One numpy array, which rows are trades and columns are [DATE, TICKER, TIMESTAMP, PRICE, SIZE]
    A second one, which rows are quotes and columns are [DATE, TICKER, TIMESTAMP, BIDPRICE, BIDSIZE, ASKPRICE, ASKSIZE]
    '''

    def __init__(self, baseDir, startDate, endDate, ticker ):
        '''
        Uses the FileManager class to get the dates, and then loops through them to build the arrays
        via one call to the methods addQuotes and addTrades.
        '''
        self._fm = FileManager( baseDir )
        
        # Retrieve list of trading days for trades & quotes files
        self._datesT = np.sort(self._fm.getTradeDates(startDate, endDate)) # 20070620, 20070621, ...
        self._datesQ = np.sort(self._fm.getQuoteDates(startDate, endDate))

        # Ticker searched
        self._ticker = ticker
        print(self._datesQ)

        # Find sizes to allocate the right space
        lengthQ = 0
        for date in self._datesQ:
            try:
                lengthQ += self._fm.getQuotesFile(date, self._ticker).getN()
            except:
                continue
            
        lengthT = 0
        for date in self._datesT:
            try:
                lengthT += self._fm.getTradesFile(date, self._ticker).getN()
            except:
                continue
            
        
        # Stacked data for this ticker
        self._stackedQuotes = np.empty((lengthQ,7), dtype=object)
        self._stackedTrades = np.empty((lengthT,5), dtype=object)
        
    # Quotes
    def addQuotes(self):
        l = 0
        for date in self._datesQ:
            try:
                quoteFile = self._fm.getQuotesFile(date, self._ticker)
            except:
                continue
            # Append the day data [DATE, TICKER, TIMESTAMP, BIDPRICE, BIDSIZE, ASKPRICE, ASKSIZE]
            length = quoteFile.getN()
            for i in range(0, length):
                self._stackedQuotes[l + i] = np.array([date, self._ticker, int(quoteFile.getTimestamp(i)), float(quoteFile.getBidPrice(i)), float(quoteFile.getBidSize(i)), float(quoteFile.getAskPrice(i)), float(quoteFile.getAskSize(i))])
            l += length
            
    # Trades
    def addTrades(self):
        l = 0
        for date in self._datesT:
            try:
                tradeFile = self._fm.getTradesFile(date, self._ticker)
            except:
                continue
            # Append the day data [DATE, TICKER, TIMESTAMP, PRICE, SIZE]
            length = tradeFile.getN()
            for i in range(0, length):
                self._stackedTrades[l + i] = np.array([date, self._ticker, int(tradeFile.getTimestamp(i)), float(tradeFile.getPrice(i)), float(tradeFile.getSize(i))])
            l += length
            
    # Returns the array of stacked adjusted trades   
    def getStackedTrades(self):
        return self._stackedTrades
    
    # Returns the array of stacked adjusted quotes
    def getStackedQuotes(self):    
        return self._stackedQuotes
