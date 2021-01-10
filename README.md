kiwoom/src/bunbong.py : 분봉데이터 호출해서 json file 만드는 코드
codes/insert_mongo_bunbong.sh : json file 을 mongodb collection에 넣는 코드

site-packages > kiwoom_api > kiwoom.py > 277L, 348L 수정할 것 (여러 계좌정보 처리)

실제 accNo 호출 시에는 첫번째 계좌의 경우 [0], 두번째 계좌의 경우 [1] 식으로 호출
예제
 -     kiwoom = Kiwoom()  # Kiwoom 인스턴스 생성
 -     kiwoom.commConnect()  # API 접속
 -     print('kiwoom.accNo : ', kiwoom.accNo) # 전체 계좌 Dict
 -     accNo=kiwoom.accNo[0]
