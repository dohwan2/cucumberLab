# 과거 데이터 긁어오기
import os
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup
import xmltodict
import json
import datetime

def get_daily_stock_price(stockCode, name, count):
    url = f'https://fchart.stock.naver.com/sise.nhn?symbol={stockCode}&timeframe=day&count={count}&requestType=0'
    rs = requests.get(url)
    dt = xmltodict.parse(rs.text)
    js = json.dumps(dt, indent=4)
    js = json.loads(js)
    data = pd.json_normalize(js['protocol']['chartdata']['item'])
    df = data['@data'].str.split('|', expand=True)
    df.columns = ['date', 'open', 'high', 'low', 'close', 'Volume']
    df = df.astype({"open":int, "high": int, "low": int, "close": int, "Volume": int})
    df['average'] = round((df['high'] + df['low'])/2, 0)
    #df = df.set_index('date')
    return df

def get_past_stock_price(days):
    print("시작합니다 {}".format(datetime.datetime.now()))
    stock_code = pd.read_csv('/home/ubuntu/files/codes.csv', converters={'종목코드':str})
    stock_code = stock_code[['종목코드', '기업명']]
    for index, row in stock_code.iterrows():
        print("{} : {}".format(row['종목코드'], datetime.datetime.now()))
        tmp = []
        tmp.append(get_daily_stock_price(row['종목코드'], row['기업명'], str(days)))
        df_final = pd.concat(tmp)
        result = {'code' : row['종목코드'], 'name' : row['기업명'], 'data': df_final.to_dict('records')}
        with open('/home/ubuntu/files/past_stock_price_json/{}_{}days_stockprice.json'.format(row['종목코드'], str(days)), 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
    print("종료합니다 {}".format(datetime.datetime.now()))
    #df_final.to_csv('/home/ubuntu/files/{}days_before_stockprice.csv'.format(row['종목코드'], str(days)), encoding='euc-kr')

if __name__=="__main__":
    get_past_stock_price(377)
    sys.exit()
