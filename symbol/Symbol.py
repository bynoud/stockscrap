from lightweight_charts import Chart
import pandas as pd
import pandas_ta as ta
from datetime import datetime
import logging, os
from pathlib import Path

from scrapper import Vndirect
from indicators import AccumulateProfit


class Symbol:
    def __init__(self, name: str, localdir = 'localdata'):
        self._name = name.upper()
        self.df = self.getPrices(localdir)

    @property
    def name(self):
        return self._name
    
    def getPrices(self, localpath):
        fname = f"{localpath}/{datetime.today().strftime('%Y-%m-%d')}"
        Path(fname).mkdir(parents=True, exist_ok=True)

        fname = f'{fname}/{self._name}.csv'
        try:
            df = pd.read_csv(fname)
            logging.debug(f'Loaded {self._name} from {fname}')
        except FileNotFoundError:
            logging.debug(f'fetching {self._name} ...')
            df = Vndirect.getPrice1Y(self._name)
            df.to_csv(fname)
        return df
    
    def __indicators(self, iname, func, *args):
        if iname in self.df:
            return
        self.df[iname] = func(*args)

    def accumulate_profit(self, window):
        self.__indicators(f'acc_profit:{window}',
                          AccumulateProfit.accumulate_profit, self.df, window)

    def rsi(self, window):
        self.__indicators(f'rsi:{window}', self.df.ta.rsi, window)
