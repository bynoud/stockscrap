
from datetime import date, datetime, timedelta
import requests, json
import pandas as pd
from scrapper.DataStruct import StockPrice, ConnectionError, ParsingError

_S = requests.Session()
_S.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'})

# Scrap this: https://dstock.vndirect.com.vn/lich-su-gia/GVR
# r=Vndirect._S.get('https://finfo-api.vndirect.com.vn/v4/stock_prices?sort=date&q=code:GVR~date:gte:2024-05-20~date:lte:2024-05-25&size=15&page=1')
_PAGE_PER_REQ = 200
def _query(sym, start, end):
    s = 'https://finfo-api.vndirect.com.vn/v4/stock_prices?sort=date'
    start = start.strftime("%Y-%m-%d") if isinstance(start, date) else start
    end = end.strftime("%Y-%m-%d") if isinstance(end, date) else end
    s = s + f'&q=code:{sym}'
    s = s + f'~date:gte:{start}~date:lte:{end}'
    s = s + f'&size={_PAGE_PER_REQ}'
    return s

def _getAllPages(query):
    page = 1
    npage = -1
    totalEle = -1
    while True:
        q = query + f'&page={page}'
        print(f'query {q}')
        r = _S.get(q)
        if r.status_code != 200:
            raise ConnectionError(f'Status code {r.status_code}')
        
        j = json.loads(r.text)
        if page == 1:
            try:
                npage = j['totalPages']
                totalEle = j['totalElements']
            except KeyError:
                raise ConnectionError('No totalPages/totalElements found')

        yield j['data']

        if page >= npage:
            break

        page += 1


def getPrice(symbol: str, startdate: date | str, enddate: date | str) -> pd.DataFrame:
    webHeader  = 'adOpen adClose adHigh adLow adAverage ceilingPrice floorPrice adChange nmVolume date'.split()
    dataHeader = '  open   close   high   low   average ceiling      floor      change   volume   time'.split()
    q = _query(symbol, startdate, enddate)
    r = _S.get(q)
    if r.status_code != 200:
        raise ConnectionError(f'Status code {r.status_code}')

    prices = []
    for data in _getAllPages(_query(symbol, startdate, enddate)):
        for d in data:
            if d['code'] != symbol:
                raise ParsingError(f'Return symbol not matched exp {symbol} <> {d["code"]}')
            prices.append(list(map(lambda k: d[k], webHeader)))
    
    df = pd.DataFrame(prices, columns=dataHeader)
    return df[::-1].reset_index(drop=True) # API return [0] as latest data

def getPrice1Y(symbol: str, dayago=365):
    end = datetime.today()
    start = end - timedelta(days=dayago)
    return getPrice(symbol, start, end)

