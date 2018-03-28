import numpy as np
import pandas as pd

class AdjustingHashmap(object):
    '''
    Dictionnary of dictionnary which allows to map a stock and a date to
    a price multiplier and a volume multiplier.
    '''

    def __init__(self, s_p500):
        '''
        s_p500: String path to the s_p500.xlsx file
        '''
        # Instantiate attributes
        self._s_p500xls = pd.read_excel(open(s_p500,'rb'), sheet_name='WRDS')

        # Main dictionary
        self._map = {}

        # Main keys = stock tickers
        self._key_tickers = self._s_p500xls['Ticker Symbol'].unique()
        self._key_tickers = np.apply_along_axis(lambda y: [str(i) for i in y], 0, self._key_tickers)
        self._key_tickers = self._key_tickers[self._key_tickers != 'nan']
        
        # Secondary keys = dates
        self._key_dates = self._s_p500xls['Names Date'].unique()
        self._key_dates = np.apply_along_axis(lambda y: [str(i) for i in y], 0, self._key_dates)
        self._key_dates = self._key_dates[self._key_dates != 'nan']
        self._key_dates = np.apply_along_axis(lambda y: [i[:-2] for i in y], 0, self._key_dates)
        
        # Fill the main and the sub-dictionaries
        self.fillDictionary()
        
    # Map the multipliers
    def fillDictionary(self):
        for ticker in self._key_tickers:
            self._map[ticker] = {}
            for date in self._key_dates:
                # Skip when not existing
                try:
                    row = self._s_p500xls.loc[(self._s_p500xls['Names Date'] == float(date)) & (self._s_p500xls['Ticker Symbol'] == ticker)].iloc[0]
                except:
                    continue
                self._map[ticker][date] = [float(row['Cumulative Factor to Adjust Prices']), float(row['Cumulative Factor to Adjust Shares/Vol'])]
                
    def getPriceMultiplier(self, ticker, date):
        return(self._map[ticker][date][0])

    def getVolMultiplier(self, ticker, date):
        return(self._map[ticker][date][1])
    
    def setPriceMultiplier(self, ticker, date, val):
        self._map[ticker][date][0] = val

    def setVolMultiplier(self, ticker, date, val):
        self._map[ticker][date][1] = val
    