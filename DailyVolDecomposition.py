import pandas as pd
import numpy as np
import logging
from bs4 import BeautifulSoup as bs
from urllib2 import urlopen


def get_shares_outstanding(symbol):
    """
    retrieve shares outstanding from Finviz.com
    fantastic stock screener on that site if I may say

    :param symbol: the company ticker symbol
    :return: the company's shares outstanding as stated from finviz.com
    """

    finviz_url = "http://www.finviz.com/quote.ashx?t="
    stock_url = finviz_url + symbol
    soup = bs(urlopen(stock_url))
    table = soup.find('table', attrs={'class': 'snapshot-table2'})

    shrs_outstand = ''

    for row in table.find_all('tr'):
        data = [td.get_text() for td in row.find_all('td')]
        if 'Index' == data[0]:
            shrs_outstand = data[9]

    #convert to a million or billion shares
    if shrs_outstand[-1] == 'M':
        num = float(shrs_outstand[:-1])
        shares_outstanding = num * 1000000
    else:
        num = float(shrs_outstand[:-1])
        shares_outstanding = num * 1000000000

    return shares_outstanding

def calculate(frame,shares_outstanding):
    """
    calculate daily RV/BV/Diff price/volume values from minute price data frame

    :param frame: pandas dataframe object from minute price data
    :param shares_outstanding: company shares outstanding for volume normalization
    :return: the new frame constructed from RV/BV values
    """

    def date_offsets(frame):
        #price dates are extremely varied
        #cannot rely on simply estimating exact dates
        #need frame date offsets

        first_date = frame['Date'][0]
        list_of_date_offsets = [0]
        counter = 0

        for date in frame['Date']:
            if date != first_date:
                first_date = date
                list_of_date_offsets.append(counter)
            counter += 1

        return list_of_date_offsets

    def single_day_log_returns(five_min_prices):

        log_five_min_returns = [np.log((f / p)) for f, p in zip(five_min_prices[1:], five_min_prices)]

        return log_five_min_returns

    def single_day_standard_volume_returns(five_min_volume):
        #standardize volume by shares outstanding

        sfmvolumes = [(x / shares_outstanding) for x in five_min_volume]
        volume_returns = [f - p for f, p in zip(sfmvolumes[1:], sfmvolumes)]

        return volume_returns

    def realized_variation(X):
        pre_log = sum([x ** 2 for x in X][1:])
        #check for log(0)
        try:
            RV = np.log(pre_log)
        except:
            RV = np.nan

        return RV

    def bipower_variation(X):
        u = np.sqrt(np.pi / 2) ** -2
        pre_log = u * sum([abs(f) * abs(p) for f, p in zip(X[2:], X[1:])])

        #check for log(0)
        try:
            BV = np.log(pre_log)
        except:
            BV = np.nan

        return BV

    def one_day_five_min_values(sub_loop_end, sub_frame):

        one_day_five_min_prices = []
        one_day_five_min_volumes = []
        price_append = one_day_five_min_prices.append
        volume_append = one_day_five_min_volumes.append
        position = sub_frame.iloc

        for k in range(0, sub_loop_end):
            if position[k]['Time'] % 5 == 0:
                price_append(position[k]['Close'])
                volume_append(position[k]['Volume'])

        return one_day_five_min_prices, one_day_five_min_volumes

    date_offsets = date_offsets(frame)
    row_length = frame.shape[0]
    #to add last row for iteration
    date_offsets.append(row_length)
    date_length = len(date_offsets)
    values = []

    for i in range(1,date_length):
        start = date_offsets[i - 1]
        end = date_offsets[i]
        sub_loop_end = end - start
        single_day_five_min_prices, single_day_five_min_volumes = one_day_five_min_values(sub_loop_end, frame[start:end])


        #price
        log_returns = single_day_log_returns(single_day_five_min_prices)
        rv = realized_variation(log_returns)
        bv = bipower_variation(log_returns)

        # error checking
        if rv or bv is not np.nan:
            diff = rv - bv
        else:
            diff = np.nan

        #volume
        volume_returns = single_day_standard_volume_returns(single_day_five_min_volumes)

        vrv = realized_variation(volume_returns)
        vbv = bipower_variation(volume_returns)

        #error checking
        if vrv or vbv is not np.nan:
            vdiff = vrv - vbv
        else:
            vdiff = np.nan

        total_volume = sum(single_day_five_min_volumes)
        close_price = frame.iloc[end - 1]['Close']

        values.append([frame.iloc[start]['Date'], rv, bv, diff, vrv,
                           vbv, vdiff, close_price,total_volume])


    new_frame = pd.DataFrame(values)
    new_frame.columns = ['Date', 'PriceTotalVol', 'PriceContinuousVol', 'PriceJumpVol',
                         'VolumeTotalVol', 'VolumeContinuousVol', 'VolumeJumpVol', 'ClosePrice', 'TotalVolume']

    return new_frame

def process(symbol):
    """
    main data generating process
    get shares outstanding then calculate RV/BV values
    then save all data to CSV file in Volatility Data/

    :param symbol: company ticker symbol
    :return: None, file will be saved or errors will be logged
    """

    path = 'Minute Prices/%s.csv' % symbol
    
    try:
        shares_outstanding = get_shares_outstanding(symbol)
        
    except Exception as e:
        logging.error('%s had error: %s' % (symbol,e))
        return None

    try:
        frame = pd.DataFrame(pd.read_csv(path))
        new_frame = calculate(frame, shares_outstanding)
        save_path = 'Volatility Data/' + symbol + '_values.csv'
        new_frame.to_csv(save_path)
        logging.info('%s saved' % symbol)

    except Exception as e:
        logging.error('%s had error: %s' % (symbol,e))
        return None

    return None
