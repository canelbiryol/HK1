import unittest
import numpy as np
from adjustAndClean.TAQAdjust import TAQAdjust
from adjustAndClean.TAQCleaner import TAQCleaner
from dbReaders.TAQQuotesReader import TAQQuotesReader
from dbReaders.TAQTradesReader import TAQTradesReader

class Test_WriteBinaryMethods(unittest.TestCase):
    '''
    This class tests the functionality of the methods addQuotes and addTrades of the class StackData.
    It works on the base directory provided by the user, and apply them to the IBM ticker.
    '''

    def test1(self):
        # Stocks and trades
        s_p500 = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/s_p500.xlsx'
        stackedTrades = np.array([['20070620', 'IBM', 34241000, 106.5, 85200.0], ['20070621', 'IBM', 57596000, 106.61000061035156, 500.0], ['20070621', 'IBM', 57596000, 106.61000061035156, 200.0], ['20070621', 'IBM', 57597000, 106.5999984741211, 200.0], ['20070621', 'IBM', 57597000, 106.5999984741211, 200.0], ['20070621', 'IBM', 57597000, 106.5999984741211, 200.0]])
        stackedQuotes = np.array([['20070620', 'IBM', 34241000, 106.5, 85200.0, 106.1, 8200.0], ['20070621', 'IBM', 57597000, 106.5, 85200.0, 106.1, 800.0], ['20070621', 'IBM', 57597000, 106.5, 85200.0, 106.1, 800.0], ['20070621', 'IBM', 57597000, 106.5, 85200.0, 106.1, 800.0], ['20070621', 'IBM', 57597000, 106.5, 85200.0, 106.1, 800.0]])
        
        # Directories where to store
        filepathadj = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/adj/'
        filepathcln = '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/cln/'
        
        # Write after reading and adjusting
        adjuster = TAQAdjust( stackedQuotes, stackedTrades, s_p500 )
        adjuster.setPriceMult("20070621", 0.5)
        adjuster.setVolMult("20070621", 0.25)
        adjuster.adjustQuote()
        adjuster.adjustTrade()
        adjuster.storeAdjustedQuotes(filepathadj)
        adjuster.storeAdjustedTrades(filepathadj)
        
        # Write after reading and cleaning
        cleaner = TAQCleaner(stackedQuotes, stackedTrades)
        stackedQuotes = np.delete(stackedQuotes, cleaner.cleanQuotesIndices(), axis = 0)
        stackedTrades = np.delete(stackedTrades, cleaner.cleanTradesIndices(), axis = 0)
        cleaner.storeCleanedQuotes(filepathcln)
        cleaner.storeCleanedTrades(filepathcln)
        
        # Read results
        readerclnQ = TAQQuotesReader( '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/cln/quotes/20070620/IBM_quotes.binRQ' )
        readerclnT = TAQTradesReader( '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/cln/trades/20070620/IBM_trades.binRT' )
        readeradjQ = TAQQuotesReader( '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/adj/quotes/20070620/IBM_quotes.binRQ' )
        readeradjT = TAQTradesReader( '/media/louis/DATA/documents/cours/NYU/SPRING_18/ATQS/HK1/adj/trades/20070620/IBM_trades.binRT' )
        
        # Using previously tested readers, test for expected values
        self.assertEquals( readerclnQ.getN(), 5 )
        self.assertEquals( readerclnQ.getSecsFromEpocToMidn(), 0 )
        self.assertEquals( readerclnQ.getMillisFromMidn( readerclnQ.getN() - 1 ), 57597000 )
        self.assertEquals( readerclnQ.getBidSize( readerclnQ.getN() - 1 ), 21300 )
        self.assertEquals( readerclnQ.getAskSize( readerclnQ.getN() - 1 ), 200 )
        self.assertAlmostEquals( readerclnQ.getAskPrice( readerclnQ.getN() - 1 ), 53.0499, 3 )
        self.assertAlmostEquals( readerclnQ.getBidPrice( readerclnQ.getN() - 1 ), 53.25, 3 )
        
        # Using previously tested readers, test for expected values
        self.assertEquals( readeradjQ.getN(), 5 )
        self.assertEquals( readeradjQ.getSecsFromEpocToMidn(), 0 )
        self.assertEquals( readeradjQ.getMillisFromMidn( readeradjQ.getN() - 1 ), 57597000 )
        self.assertEquals( readeradjQ.getBidSize( readeradjQ.getN() - 1 ), 21300 )
        self.assertEquals( readeradjQ.getAskSize( readeradjQ.getN() - 1 ), 200 )
        self.assertAlmostEquals( readeradjQ.getAskPrice( readeradjQ.getN() - 1 ), 53.0499, 3 )
        self.assertAlmostEquals( readeradjQ.getBidPrice( readeradjQ.getN() - 1 ), 53.25, 3 )
        
        # Using previously tested readers, test for expected values
        self.assertEquals( readerclnT.getN(), 6 )
        self.assertEquals( readerclnT.getSecsFromEpocToMidn(), 0 )
        self.assertEquals( readerclnT.getMillisFromMidn( readerclnT.getN() - 1 ), 57597000 )
        self.assertEquals( readerclnT.getSize( readerclnT.getN() - 1 ), 50 )
        self.assertAlmostEquals( readerclnT.getPrice( readerclnT.getN() - 1 ), 53.29999, 3 )
        
        # Using previously tested readers, test for expected values
        self.assertEquals( readeradjT.getN(), 6 )
        self.assertEquals( readeradjT.getSecsFromEpocToMidn(), 0 )
        self.assertEquals( readeradjT.getMillisFromMidn( readeradjT.getN() - 1 ), 57597000 )
        self.assertEquals( readeradjT.getSize( readeradjT.getN() - 1 ), 50 )
        self.assertAlmostEquals( readerclnT.getPrice( readeradjT.getN() - 1 ), 53.29999, 3 )
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test1']
    unittest.main()