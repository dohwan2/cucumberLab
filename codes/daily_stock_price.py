import os
import sys
import pymongo
import pandas as pd
import requests
from bs4 import BeautifulSoup
import xmltodict
import json

ip = 'localhost'
port = 27017
db_name = 'trading'
collection_name = 'stock-price'

def get_daily_stock_price(stockCode):
    url = f'https://fchart.stock.naver.com/sise.nhn?symbol={stockCode}&timeframe=day&count=1&requestType=0'
    rs = requests.get(url)
    dt = xmltodict.parse(rs.text)
    js = json.dumps(dt, indent=4)
    js = json.loads(js)
    data = pd.json_normalize(js['protocol']['chartdata']['item'])
    df = data['@data'].str.split('|', expand=True)
    df.columns = ['date', 'open', 'high', 'low', 'close', 'Volume']
    df = df.astype({"open":int, "high": int, "low": int, "close": int, "Volume": int})
    df['average'] = round((df['high'] + df['low'])/2, 0)
    result = df.to_dict('records')
    return result

def mongo_connection():
    # Connect MongoDB
    connection = pymongo.MongoClient(ip, port)

    # Connect MongoDB Database
    database = connection.get_database(db_name)

    # Connect MongoDB Database Collection
    collection = database.get_collection(collection_name)

    # find Data
    docs = collection.find()
    for doc in docs:
        new_data = get_daily_stock_price(doc['code'])[0]
        data = doc['data']

        #지금 넣으려는 날짜의 기존 데이터에 없는 경우에만
        if data[-1]['date'] != new_data['date']:
            #제일 오래 된 날짜는 제외
            data = data[1:]
            data.append(new_data)
            collection.update_one({'_id':doc['_id']}, {'$set': {'data': data}})

if __name__=="__main__":
    mongo_connection()
    sys.exit()
