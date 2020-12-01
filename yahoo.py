# https://pypi.org/project/yfinance/
import yfinance as yf
from datetime import datetime, timedelta

def num_to_timestr(s):
    if s < 10:
        return '0{0}'.format(s)
    return '{0}'.format(s)

# tickers == [ticker:str, price: null, [year:int, month:int, day:int], [hour:int, min:int, sec:int]]
def get_prices(tickers):
    pricedata = []
    for item in tickers:
        ticker, price, date, time = item
        year, month, day = date
        hour, minute, second = time
        next_date = datetime(year, month, day) + timedelta(days=1)

        # guard against future dates
        if datetime(year, month, day) > datetime.now(): 
            pricedata.append(item) 
            continue

        data = yf.download(
            tickers=ticker,
            interval="1m",
            start="{0}-{1}-{2}".format(year, month, day),
            end="{0}-{1}-{2}".format(next_date.year,
                                     next_date.month, next_date.day)
        )
        # check if ticker was not found
        if data.empty:
            pricedata.append(item) 
            continue

        # extract by time
        datestring = "{0}-{1}-{2} {3}:{4}:{5}".format(year, month, day,
                                                      num_to_timestr(hour),
                                                      num_to_timestr(minute),
                                                      #   num_to_timestr(second),
                                                      '00'
                                                      )
        
        # guard against accessing unavailable index
        if not datestring in data.index:
            pricedata.append(item) 
            continue
        # pick the price
        data = data.loc[datestring]
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_json.html
        data = [ticker, data['Close'], date, time]
        pricedata.append(data)

    return pricedata

