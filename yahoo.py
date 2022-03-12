# https://pypi.org/project/yfinance/
import yfinance as yf
from datetime import datetime, timedelta

logging = True


def num_to_timestr(s):
    if s < 10:
        return '0{0}'.format(s)
    return '{0}'.format(s)

# tickers == [ticker:str, price: null, [year:int, month:int, day:int], [hour:int, min:int, sec:int]]
# if attach_prices == True, we attach all available prices


def get_prices(tickers, attach_prices=False):
    pricedata = []
    for item in tickers:
        ticker, price, date, time = item
        year, month, day = date
        hour, minute, second = time
        next_date = datetime(year, month, day) + timedelta(days=1)

        # check calendar
        if year > datetime.now().year or year < 1900:
            item.append({
                "errors": ["Invalid year number"]
            })
            pricedata.append(item)
            continue

        if month > 12 or month < 1:
            item.append({
                "errors": ["Invalid month number"]
            })
            pricedata.append(item.append({
                "errors": ["Invalid month number"]
            }))
            continue

        if day > 31 or day < 1:
            item.append({
                "errors": ["Invalid day number"]
            })
            pricedata.append(item.append({
                "errors": ["Invalid day number"]
            }))
            continue

        # TODO Guard for Saturdays/Sundays

        # guard against future dates
        if datetime(year, month, day) > datetime.now():
            pricedata.append(item.append({
                "errors": ["Future date not allowed"]
            }))
            continue

        start = "{0}-{1}-{2}".format(year, month, day)
        end = "{0}-{1}-{2}".format(next_date.year,
                                   next_date.month, next_date.day)

        if logging == True:
            print('start=', start, 'end=', end)
            print('date=', date, 'next_date=', next_date)
            # print('1601506800=', datetime.fromtimestamp(1601506800).strftime("%m/%d/%Y, %H:%M:%S"),
            #   '1601593200=', datetime.fromtimestamp(1601593200).strftime("%m/%d/%Y, %H:%M:%S"))

        # download prices
        df = yf.download(
            tickers=ticker,
            interval="1m",
            start=start,
            end=end
        )
        
        if logging == True:
            print(df.info())

        # check if ticker was not found
        if df.empty:
            item.append({
                "errors": ["Ticker was not found"]
            })
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
        if not datestring in df.index:
            print('unavailable index fired')
            item.append({
                "errors": ["1m data is unavailable for this date & time"]
            })
            pricedata.append(item)
            continue

        # pick the price
        data = df.loc[datestring]
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_json.html
        data = [ticker, data['Close'], date, time]

        if attach_prices == True:
            data.append(df.to_json())

        pricedata.append(data)
    return pricedata
