import unittest
from dbReaders.TAQTradesReader import TAQTradesReader
from partB.TAQStats import TAQStats
from partB.xMinuteReturn import getXSecTradeReturns, getXSecMidQuoteReturns
from dbReaders.TAQQuotesReader import TAQQuotesReader
from adjustAndClean.StackData import StackData

class Test_TAQStats(unittest.TestCase):

    def testXMinuteReturns(self):
        taqBaseDir = "/Users/canelbiryol/Documents/sampleTAQ/"
        filePathName = "trades/20070620/IBM_trades.binRT"
        
        data = TAQTradesReader( taqBaseDir + filePathName )
        #print( "%s" % (getXMinuteTradeReturns(data, 30)))

    def testStats(self):

        baseDir = "/Users/canelbiryol/Documents/SampleTAQ"
        startDate = "20070620"
        endDate = "20070621"
        ticker = 'IBM'
        seconds = 60
        
        stack = StackData(baseDir, startDate, endDate, ticker)
        stack.addTrades()
        stack.addQuotes()
        quotes = stack.getStackedQuotes()
        trades = stack.getStackedTrades()
        
        taqstats = TAQStats(trades, quotes, seconds)
       
        self.assertTrue(taqstats.getSampleLength() == 1 )
        self.assertTrue(taqstats.getNumofTrades() == 23595 )
        self.assertTrue(taqstats.getNumofQuotes() == 68489 )
        self.assertTrue(taqstats.getTradestoQuotes() == 0.3445078771773569 )
        
        self.assertTrue(taqstats.getTradeMeanReturns() == -0.0027798923776834253 )
        self.assertTrue(taqstats.getTradeMedianReturns() == 0.0 )
        self.assertTrue(taqstats.getTradeStdReturns() == 0.006959876228605448 )
        self.assertTrue(taqstats.getTradeMedianAbsDev() == 0.06004653651674152 )
        self.assertTrue(taqstats.getTradeSkew() == -8.732089543946557 )
        self.assertTrue(taqstats.getTradeKurtosis() == 645.0738400540301 )
        self.assertTrue(taqstats.get10largestTrade() == [0.0015987789524862794, 0.0013664916570730323, 0.0013192554280530011, 0.0012233883945467205, 0.0012221232496127943, 0.0011264690505690123, 0.001125729346151516, 0.0010350076365732708, 0.0010323848634534727, 0.00103161036467192] )
        self.assertTrue(taqstats.get10smallestTrade() == [-0.002158845081256966, -0.0017848268431994718, -0.0013126477989491292, -0.001129047032044861, -0.0010352024105038105, -0.0010310301605999106, -0.000940365596810322, -0.0009399236271715461, -0.0008450283117076296, -0.0008433655008963648] )
        
        self.assertTrue(taqstats.getQuoteMeanReturns() == -0.002566885742490683 )
        self.assertTrue(taqstats.getQuoteMedianReturns() == 0.0 )
        self.assertTrue(taqstats.getMidQuoteStdReturns() == 0.006988520545323737 )
        self.assertTrue(taqstats.getMidQuoteMedianAbsDev() == 0.047447428528355484 )
        self.assertTrue(taqstats.getMidQuoteSkew() == -13.778696482956754 )
        self.assertTrue(taqstats.getMidQuoteKurtosis() == 727.42264590066)
        self.assertTrue(taqstats.get10largestMidQuote() == [0.0014575773845633133, 0.0014135391679692688, 0.0014098550235774887, 0.0013175172862216478, 0.001314548259609749, 0.0012202090012962685, 0.0011762491715587853, 0.0011716187234882547, 0.0011256765357847698, 0.0010810968598524706] )
        self.assertTrue(taqstats.get10smallestMidQuote() == [-0.0021589106168465877, -0.0018786112151241152, -0.0012656647923097175, -0.0011761026226797533, -0.0010823177950285423, -0.001030981870436265, -0.0009868841748631452, -0.0009388205857776555, -0.0008932945443891338, -0.0008899471352890043] )
        
 
      

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testVWAP']
    unittest.main()