from lightweight_charts import Chart
import pandas as pd
import pandas_ta as ta
from datetime import datetime
from scrapper import Vndirect
from indicators import AccumulateProfit

WIN = 50
WIN2 = 20
# if profit 100 < profit50 < profit 20 < 0, and all of them in recover >=0
# then maybe it's a good indicator?

SYM = 'BCG'

chart = Chart(inner_width=1, inner_height=0.4, toolbox=True)
chart.time_scale(visible=False)

chart2 = chart.create_subchart(width=1, height=0.4, sync=True)
line = chart2.create_line('acc_profit_perc:100', color='AntiqueWhite')
line5 = chart2.create_line('acc_profit_perc:50', color='Aquamarine')
line6 = chart2.create_line('acc_profit_perc:20', color='BlueViolet')
line2 = chart2.create_line('zero')

chart3 = chart.create_subchart(width=1, height=0.2, sync=True)
line3 = chart3.create_line('rsi')
line4 = chart3.create_line('const50')

chart.set(bcg.df)
line.set(bcg.df)
line2.set(bcg.df)
line5.set(bcg.df)
line6.set(bcg.df)
line3.set(bcg.df)
line4.set(bcg.df)

# if __name__ == '__main__':

#     chart = Chart(inner_width=1, inner_height=0.4, toolbox=True)
#     chart.time_scale(visible=False)

#     chart2 = chart.create_subchart(width=1, height=0.4, sync=True)
#     line = chart2.create_line('acc_profit_perc:100', color='AntiqueWhite')
#     line5 = chart2.create_line('acc_profit_perc:50', color='Aquamarine')
#     line6 = chart2.create_line('acc_profit_perc:20', color='BlueViolet')
#     line2 = chart2.create_line('zero')

#     chart3 = chart.create_subchart(width=1, height=0.2, sync=True)
#     line3 = chart3.create_line('rsi')
#     line4 = chart3.create_line('const50')

#     # fname = datetime.today().strftime('%Y-%m-%d')
#     # fname = f'localdata/{SYM}.{fname}.csv'
#     # try:
#     #     df = pd.read_csv(fname)
#     #     print('Loaded {SYM} from {fname}')
#     # except FileNotFoundError:
#     #     print('fetching')
#     #     df = Vndirect.getPrice1Y(SYM)
#     #     df.to_csv(fname)
#     #     print('Fetched {SYM}')
    
#     # # # df = pd.read_csv('gvr1y.csv')
#     # # df = Vndirect.getPrice('KSB', '2023-05-25', '2024-05-27')
#     # # df.to_csv('ksb1y.csv')
#     # # # df = pd.read_csv('ksb1y.csv')

#     # AccumulateProfit.accumulate_profit(df,WIN)
#     # AccumulateProfit.accumulate_profit(df,WIN2)
#     # AccumulateProfit.accumulate_profit(df,100)
#     # df['rsi'] = df.ta.rsi(WIN)
#     # df['zero'] = 0
#     # df['const50'] = 50


#     # chart.set(df)
#     # line.set(df)
#     # line2.set(df)
#     # line5.set(df)
#     # line6.set(df)
#     # line3.set(df)
#     # line4.set(df)

#     chart.show(block=False)


