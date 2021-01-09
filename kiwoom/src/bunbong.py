## JY : 일분봉 가져오는 코드

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import *
from kiwoom_api.api import Kiwoom, DataFeeder, Executor
from kiwoom_api.utility import utility
import sys
import pandas as pd
import datetime

if __name__ == "__main__":
    app = QApplication(sys.argv)

    kiwoom = Kiwoom()  # Kiwoom 인스턴스 생성
    kiwoom.commConnect()  # API 접속

    feeder = DataFeeder(kiwoom)
    executor = Executor(kiwoom)

    print('feeder.accNo : ', feeder.accNo)
    print('kiwoom.accNo : ', kiwoom.accNo)

    accNo = '8152212611'  # juyoung

    params = {
        "종목코드": "005930",
        "틱범위": 1,  # 0 연속조회여부 (0: x)
        "수정주가구분": 1,  # 종목코드 갯수
    }

    stock_code = pd.read_csv('C:/Users/Administrator/PycharmProjects/kiwoom/src/codes.csv', converters={'종목코드': str})
    stock_code = stock_code[['종목코드', '기업명']]

    #중간에 종료되었을 때 이미 쌓은 종목은 스킵하기 위함
    skipcnt = 784 + 3 #021820, 012170, 007630 못쌓음
    cnt = 0
    for index, row in stock_code.iterrows():
        cnt += 1
        if cnt > skipcnt :
            print("{} 번째 종목 ".format(cnt))
            print("{} : {}".format(row['종목코드'], datetime.datetime.now()))
            params['종목코드'] = row['종목코드']

            result = {
                'code': row['종목코드'],
                'name': row['기업명'],
                'data': []
            }

            data = feeder.requestPrev(trCode="OPT10080", isPrev=0, **params)
            result['data'] += data['멀티데이터']

            for i in range(14):
                data = feeder.requestPrev(trCode="OPT10080", isPrev=2, **params)
                result['data'] += data['멀티데이터']
                print(data['멀티데이터'][0]['체결시간'])
                QTest.qWait(700)

            print("총 데이터 수 : ", len(result['data']))

            # json 파일로 저장
            utility.writeJson(result, 'C:/Users/Administrator/PycharmProjects/kiwoom/result/bunbong/{}_13500.json'.format(row['종목코드']))

    print("종료합니다 {}".format(datetime.datetime.now()))

