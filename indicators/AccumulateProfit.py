import numpy as np
import pandas as pd

def _create_price_bins(ref, minv, maxv, step=0.01, roundto=0.05):
    # rounding
    roundv = int(1 / roundto)
    def myround(v):
        return round(v * roundv) / roundv
    
    cur = myround(ref)
    bins = [cur]
    while cur > minv:
        cur = myround(cur - (cur * step))
        bins.insert(0,cur)

    cur = myround(ref)
    while cur < maxv:
        cur = myround(cur + (cur * step))
        if cur <= maxv:
            bins.append(cur)

    return bins

def _psuedo_price_distribute(refv, minv, maxv, average, volume):
    prices = np.random.triangular(minv,average,maxv,2000)
    #prices = pd.DataFrame(np.random.triangular(minv,average,maxv,2000))
    bins = _create_price_bins(refv, minv, maxv)
    dist = pd.DataFrame(prices).groupby(pd.cut(prices, bins=bins), observed=True).count()
    return (dist * volume) / dist.sum()

def generate_price_distribution(prices: pd.DataFrame):
    refv = prices.iloc[0]['close']
    def gendist(p):
        nonlocal refv
        d = _psuedo_price_distribute(refv, p['low'], p['high'], p['average'], p['volume'])
        # print('xx', d)
        try:
            refv = d.index[0].left
        except IndexError:
            pass # d is empty
        return d
    return prices.apply(gendist, axis=1)

def price_accumulation(prices: pd.DataFrame, window:int):
    
    if window > len(prices):
        return [None]*len(prices)
    
    ret = []
    for i in range(window-1):
        ret.append(None)
    
    dist = generate_price_distribution(prices)
    
    acc = dist[0]
    for i in range(1,window):
        acc = acc.add(dist[i], fill_value=0)
    ret.append(acc)
    first = dist[0]

    for i in range(window, len(dist)):
        acc = ret[-1].add(dist[i],fill_value=0).sub(first,fill_value=0)
        ret.append(acc[acc>10].dropna()) # fix very small negative number
        first = dist[i-window+1]

    return ret

def accumulate_profit(prices: pd.DataFrame, window:int):
    # iname = f'acc_profit:{window}'
    # if iname in prices:
    #     return prices[iname]
    
    accprice = price_accumulation(prices, window)
    ret = []
    for i,acc in enumerate(accprice):
        if acc is None:
            ret.append(0)
            continue
        a = acc.reset_index(names='prange')
        profit = a.apply(lambda k: (prices.iloc[i]['close']-k['prange'].mid) * k[0], axis=1).sum()
        ret.append(profit)
    # prices['acc_profit'] = ret
    lastVal = (prices['volume'].tail(window).sum() * prices['average'].tail(window).sum()) / window
    return (pd.DataFrame(ret) * 100 / lastVal)
    # prices[iname] = ret * 100 / lastVal
    # prices['acc_profit'] = prices[iname]
    # return prices[iname]
