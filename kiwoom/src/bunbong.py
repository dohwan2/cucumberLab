import sys
from PyQt5.QtWidgets import QApplication
from kiwoom_api.api import Kiwoom, DataFeeder, Executor
from kiwoom_api.utility import utility
from datetime import datetime

if __name__ == "__main__":
    app = QApplication(sys.argv)

    kiwoom = Kiwoom()  # Kiwoom 인스턴스 생성
    kiwoom.commConnect()  # API 접속

    feeder = DataFeeder(kiwoom)
    executor = Executor(kiwoom)

    print('feeder.accNo : ', feeder.accNo)
    print('kiwoom.accNo : ', kiwoom.accNo)
    # print('feeder.getAccountDict() : ', feeder.getAccountDict("6101405841"));
    # print('kiwoom.getChejanData() : ', kiwoom.getChejanData());

    # accNo = '8151674211' #dohwan
    accNo = '8152212611' #juyoung
    code = "005930"  # 삼성전자
    # code = "036630"  # 세종텔레콤

    params = {
        "종목코드": "005930",
        "틱범위": 1,  # 0 연속조회여부 (0: x)
        "수정주가구분": 1,  # 종목코드 갯수
    }

    result = {
        'code':params["종목코드"],
        'name':'삼성전자',
        'data':[]
    }
    data = feeder.requestPrev(trCode="OPT10080", isPrev=0, **params)
    result['data'] += data['멀티데이터']

    print(datetime.now())
    for i in range(24):
        data = feeder.requestPrev(trCode="OPT10080", isPrev=2, **params)
        result['data'] += data['멀티데이터']
        print(data['멀티데이터'][0]['체결시간'])
        print(len(data['멀티데이터']))
    print(datetime.now())
    print(len(result['data']))
    utility.writeJson(result, 'C:/Users/Administrator/PycharmProjects/kiwoom/result/0109_2.json')
    #feeder.getAccountDict(feeder.accNo)
    #s8576791