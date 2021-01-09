# import sys
# from PyQt5.QtWidgets import QApplication
# from kiwoom_api.api import Kiwoom, DataFeeder
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#
#     kiwoom = Kiwoom()  # Kiwoom 인스턴스 생성
#     kiwoom.commConnect()  # API 접속
#     feeder = DataFeeder(kiwoom)
#
#     code = "005930"  # 삼성전자
#
#     # TR요청(request)에 필요한 parameter는 KOAStudio를 참고하시길 바랍니다.
#     # OPT10004: 주식호가요청
#     params = {"종목코드": code}
#     data = feeder.request(trCode="OPT10004", **params)
#     print(data)
#
#     # OPT10059: 종목별투자자기관별요청
#     params = {
#         "일자": "202003013",
#         "종목코드": code,
#         "금액수량구분": "1",  # 1:금액, 2:수량
#         "매매구분": "0",  # 0:순매수, 1:매수, 2:매도
#         "단위구분": "1",  # 1:단주, 1000:천주
#     }
#     data = feeder.request(trCode='OPT10059', **params)
#     print(data)
#
#     # OPTKWFID: 관심종목정보요청
#     # ※ 예외적으로 requestOPTKWIFID 메서드를 호출
#     params = {
#         "arrCode": "005930;023590",  # 종목코드를 ;로 구분
#         "next": 0,  # 0 연속조회여부 (0: x)
#         "codeCount": 2,  # 종목코드 갯수
#     }
#     data = feeder.request(**params)
#     print(data)

import sys
from PyQt5.QtWidgets import QApplication
from kiwoom_api.api import Kiwoom, DataFeeder, Executor
import time

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

    orderSpecDict = executor.createOrderSpec(
        rqName="test",
        scrNo="0000",
        accNo=kiwoom.accNo,
        orderType=1,  # 신규매수
        code=code,
        qty=1,
        price=0,  # 시장가 주문은 가격을 입력하지 않음
        hogaType="03",  # "00":지정가, "03":시장가
        originOrderNo="",
    )
    count = 1
    # for i in range(count):
    #     executor.sendOrder(**orderSpecDict)  # 삼성전자 1주 신규매수(시장가) 주문 제출
    #     print(i)
        # time.sleep(1)
    #time.sleep(1)
    params = {
        "종목코드": "005930",
        "틱범위": 1,  # 0 연속조회여부 (0: x)
        "수정주가구분": 1,  # 종목코드 갯수
    }

    data = feeder.request(trCode="OPT10080", **params)
    print(data)

    #feeder.getAccountDict(feeder.accNo)
    #s8576791