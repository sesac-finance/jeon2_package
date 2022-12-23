import json
import time
import yaml
import datetime
import requests
from bs4 import BeautifulSoup

# 한국투자증권 Open API key, 디스코드 웹훅 URL 설정 파일
with open('/mnt/FE0A5E240A5DDA6B/workspace/jeon2_package/TradeModule/config.yaml', encoding='UTF-8') as f:
    _cfg = yaml.load(f, Loader=yaml.FullLoader)

# 서비스 연결을 위해 홈페이지에서 발급 받은 두 가지 암호키(App Key, App Secret)를 활용하여 보안 인증키(token, refresh token)를 발급 받을 수 있음
# refresh token? token이 90일 뒤 만료될 것임으로 재발급 받위 위한 용도의 token
APP_KEY = _cfg['APP_KEY']
APP_SECRET = _cfg['APP_SECRET']

ACCESS_TOKEN = ""
URL_BASE = _cfg['URL_BASE'] # 투자 서비스 주소

CANO = _cfg['CANO'] # 종합계좌번호로 앞 8자리를 입력
ACNT_PRDT_CD = _cfg['ACNT_PRDT_CD'] # 계좌상품코드로 계좌번호의 뒤 2자리를 입력

DISCORD_WEBHOOK_URL = _cfg['DISCORD_WEBHOOK_URL']

def send_message(msg):
    """디스코드 메세지 전송"""
    now = datetime.datetime.now()
    message = {"content": f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {str(msg)}"}
    requests.post(DISCORD_WEBHOOK_URL, data=message)
    print(message)

def get_access_token(): # REST API. HTTP Method: POST
    """token 발급"""
    headers = {"content-type":"application/json"} # 컨텐츠 타입
    body = {"grant_type":"client_credentials", # requsest 요청에 포함됨
    "appkey":APP_KEY, 
    "appsecret":APP_SECRET}
    PATH = "oauth2/tokenP" # 호출할 API의 위치
    URL = f"{URL_BASE}/{PATH}"
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    ACCESS_TOKEN = res.json()["access_token"] # token 요청
    return ACCESS_TOKEN
    
def hashkey(datas): # POST로 보내는 요청(body 값)을 hashkey를 활용해 암호화
    """암호화"""
    PATH = "uapi/hashkey" # hashkey 발급 받을 주소 설정
    URL = f"{URL_BASE}/{PATH}"
    headers = {
    'content-Type' : 'application/json',
    'appKey' : APP_KEY,
    'appSecret' : APP_SECRET,
    }
    res = requests.post(URL, headers=headers, data=json.dumps(datas))
    hashkey = res.json()["HASH"] # hashkey 요청
    return hashkey

def get_current_price(code="005930"):
    """현재가 조회"""
    PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
            "authorization": f"Bearer {ACCESS_TOKEN}", # 접근 토큰
            "appKey":APP_KEY,
            "appSecret":APP_SECRET,
            "tr_id":"FHKST01010100"} # 각 API 별로 다른 거래 ID(tr_id)를 갖고 있음
    params = { # requsest 요청에 포함됨. Query params
    "fid_cond_mrkt_div_code":"J", # 시장 구분. J: 주식, ETF, ETN. W: ELW, U: 업종
    "fid_input_iscd":code, # 종목 코드
    }
    res = requests.get(URL, headers=headers, params=params)
    return int(res.json()['output']['stck_prpr']) # stck_prpr는 현재가

def get_target_price(code="005930"):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    PATH = "uapi/domestic-stock/v1/quotations/inquire-daily-price" # 주식현재가 일자별 API의 위치
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
        "authorization": f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"FHKST01010400"} # 주식현재가 일자별 API의 tr_id
    params = {
    "fid_cond_mrkt_div_code":"J",
    "fid_input_iscd":code,
    "fid_org_adj_prc":"1", # 수정주가(액면분할/액면병합 등 권리 발생 시 과거 시세를 현재 주가에 맞게 보정한 가격)가 반영된 가격 가져오기. 0: 수정주가 미반영
    "fid_period_div_code":"D" # 기간 분류 코드로 일자별 데이터를 의미. D: 일, W: 주, M: 월
    }
    res = requests.get(URL, headers=headers, params=params)
    stck_oprc = int(res.json()['output'][0]['stck_oprc']) #오늘 시가
    stck_hgpr = int(res.json()['output'][1]['stck_hgpr']) #전일 고가
    stck_lwpr = int(res.json()['output'][1]['stck_lwpr']) #전일 저가
    target_price = stck_oprc + (stck_hgpr - stck_lwpr) * 0.5 # 돌파계수 K
    return target_price

def get_stock_balance():
    """주식 잔고 조회"""
    PATH = "uapi/domestic-stock/v1/trading/inquire-balance"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC8434R", # 실전투자 주식 잔고 조회 거래 ID. VTTC8434R: 모의투자
        "custtype":"P", # 고객 타입. 개인. B: 법인
    }
    params = {
        "CANO": CANO, # 종합계좌번호
        "ACNT_PRDT_CD": ACNT_PRDT_CD, # 계좌상품코드
        "AFHR_FLPR_YN": "N", # 시간 외 단일가 여부. N: 기본값, Y: 시간 외 단일가
        "OFL_YN": "", # 오프라인 여부
        "INQR_DVSN": "02", # 조회 구분. 01: 대출일별, 02: 종목별
        "UNPR_DVSN": "01", # 단가 구분
        "FUND_STTL_ICLD_YN": "N", # 펀드 결제분 포함 여부
        "FNCG_AMT_AUTO_RDPT_YN": "N", # 융자금액 자동 상환 여부
        "PRCS_DVSN": "01", # 처리 구분. 00: 전일 매매 포함. 01: 전일 매매 미포함
        "CTX_AREA_FK100": "", # 연속 조회 검색 조건 100. 공란: 최초 조회 시
        "CTX_AREA_NK100": "" # 연속 조회 키 100. 공란: 최초 조회 시
    }
    res = requests.get(URL, headers=headers, params=params)
    stock_list = res.json()['output1']
    evaluation = res.json()['output2']
    stock_dict = {}
    send_message(f"====주식 보유잔고====")
    for stock in stock_list:
        if int(stock['hldg_qty']) > 0: # 보유 수량
            stock_dict[stock['pdno']] = stock['hldg_qty'] # 종목 코드
            send_message(f"{stock['prdt_name']}({stock['pdno']}): {stock['hldg_qty']}주") # prdt_name: 상품명
            time.sleep(0.1)
    send_message(f"주식 평가 금액: {evaluation[0]['scts_evlu_amt']}원") # 유가 평가 금액
    time.sleep(0.1)
    send_message(f"평가 손익 합계: {evaluation[0]['evlu_pfls_smtl_amt']}원") # 평가 손익 합계 금액
    time.sleep(0.1)
    send_message(f"총 평가 금액: {evaluation[0]['tot_evlu_amt']}원") # 총 평가 금액
    time.sleep(0.1)
    send_message(f"=====================")
    return stock_dict

def get_balance():
    """현금 잔고 조회"""
    PATH = "uapi/domestic-stock/v1/trading/inquire-psbl-order"
    URL = f"{URL_BASE}/{PATH}"
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC8908R",
        "custtype":"P",
    }
    params = {
        "CANO": CANO, # 종합계좌번호
        "ACNT_PRDT_CD": ACNT_PRDT_CD, # 계좌상품코드
        "PDNO": "005930", # 종목 코드
        "ORD_UNPR": "65500", # 주문 단가
        "ORD_DVSN": "01", # 주문 구분
        "CMA_EVLU_AMT_ICLD_YN": "Y", # CMA 평가 금액 포함 여부
        "OVRS_ICLD_YN": "Y" # 해외 포함 여부
    }
    res = requests.get(URL, headers=headers, params=params)
    cash = res.json()['output']['ord_psbl_cash'] # 주문 가능 현금
    send_message(f"주문 가능 현금 잔고: {cash}원")
    return int(cash)

"""
<주문 구분>
00: 지정가
01: 시장가
02: 조건부 지정가
03: 최유리 지정가
04: 최우선 지정가
05: 장전 시간 외
06: 장후 시간 외
07: 시간 외 단일가
08: 자기주식
09: 자기주식 S-Option
10: 자기주식 금전신탁
11: IOC지정가 (즉시 체결, 잔량 취소)
12: FOK지정가 (즉시 체결, 전량 취소)
13: IOC시장가
14: FOK시장가
15: IOC최유리
16: FOK최유리

* 최유리 지정가: 체결에 가장 유리한 가격으로 주문
매도 호가(파란색 영역) 중 가장 낮은 가격으로 매수, 매수 호가(빨간색 영역) 중 가장 높은 가격으로 매도

* IOC: Immediate or Cancel. 주문 즉시 미체결 수량에 대해서 취소
* FOK: Fill or Kill. 주문 물량을 모두 체결할 수 있으면 체결하고, 그렇지 않으면 1주도 체결하지 않고 취소
"""

def buy(code="005930", qty="1"):
    """주식 시장가 매수"""  
    PATH = "uapi/domestic-stock/v1/trading/order-cash"
    URL = f"{URL_BASE}/{PATH}"
    data = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "PDNO": code,
        # "ORD_DVSN": "01", # 시장가
        "ORD_DVSN": "16", # 16: FOK최유리 (즉시 체결, 전량 취소)
        "ORD_QTY": str(int(qty)), # 주문 수량
        "ORD_UNPR": "0", # 주문 단가
    }
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC0802U", # 주식 현금 매수 주문
        "custtype":"P",
        "hashkey" : hashkey(data) # 요청 암호화
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))
    if res.json()['rt_cd'] == '0': # 성공 실패 여부. 0: 성공, 0 이외의 값: 실패
        send_message(f"[매수 성공]{str(res.json())}")
        return True
    else:
        send_message(f"[매수 실패]{str(res.json())}")

        # try: # Ver. 5

            # send_message(type(str(res.json())))

            # symbol_list.remove(sym) # added for an improvement on 10/19. Ver. 1
            # symbol_list = symbol_list

        # del sym # added for an improvement on 11/2. Ver. 2

        # if {str(res.json())} == {'rt_cd': '7', 'msg_cd': 'APBK1680', 'msg1': '해당종목은 교육이수가 등록/승인된 계좌만 매수주문가능합니다'}: # Ver. 3
        #     symbol_list.remove(sym)

        # if 'APBK1680' in str(res.json()): # Ver. 4
        #     symbol_list.remove(sym)
        
        # except:
        #     return False
        return False

def sell(code="005930", qty="1"):
    """주식 시장가 매도"""
    PATH = "uapi/domestic-stock/v1/trading/order-cash"
    URL = f"{URL_BASE}/{PATH}"
    data = {
        "CANO": CANO,
        "ACNT_PRDT_CD": ACNT_PRDT_CD,
        "PDNO": code,
        # "ORD_DVSN": "01", # 시장가
        "ORD_DVSN": "15", # 15: IOC최유리 (즉시 체결, 잔량 취소)
        "ORD_QTY": qty, # 주문 수량
        "ORD_UNPR": "0", # 주문 단가
    }
    headers = {"Content-Type":"application/json", 
        "authorization":f"Bearer {ACCESS_TOKEN}",
        "appKey":APP_KEY,
        "appSecret":APP_SECRET,
        "tr_id":"TTTC0801U", # 주식 현금 매도 주문
        "custtype":"P",
        "hashkey" : hashkey(data) # 요청 암호화
    }
    res = requests.post(URL, headers=headers, data=json.dumps(data))
    if res.json()['rt_cd'] == '0': # 성공 실패 여부
        send_message(f"[매도 성공]{str(res.json())}")
        return True
    else:
        send_message(f"[매도 실패]{str(res.json())}")
        return False

def StockCrawler():
    """네이버 금융_국내증시_거래상위_코스피 탭에서 거래량 내림차순 순으로 주식 종목코드 5개를 가져옵니다.
    \n조건 1. 인버스/레버리지 ETF 제외
    \n조건 2. 현재가 <= 주문 가능한 현금 잔고 // 5
    """

    URL = 'https://finance.naver.com/sise/sise_quant.nhn'
    res = requests.get(URL)

    soup = BeautifulSoup(res.text, 'lxml') # html.parser
    stocks = soup.select('.type_2 tr')[2:]
    
    codes = []

    blance = get_balance() # 추가
    counts = 10 # 추가
    
    for stock in stocks:
        try:
            stock_n = stock.select_one('.tltle').text
            price = stock.select_one('.number').text.replace(',', '')
            code = stock.select_one('.tltle').attrs['href'][-6:]

            # if (('인버스' not in stock_n) and ('레버리지' not in stock_n)) and (int(price) <= (blance / counts)): # default
            # if int(price) <= (blance / counts): # added for an improvement on 9/29
            if int(price) <= 30000: # added for an improvement on 10/7
                codes.append(code)
            else:
                pass
        except:
            continue

        if len(codes) == counts:
            break
        
    return list(codes)

# 자동매매 시작
try:
    ACCESS_TOKEN = get_access_token() # 보안 인증키 발급
    symbol_list = StockCrawler() # 매수 대상 종목 리스트
    bought_list = [] # 매수 완료된 종목 리스트
    total_cash = get_balance() # 현금 잔고 조회
    stock_dict = get_stock_balance() # 주식 잔고 조회. {"종목 번호": 보수 수량}
    for sym in stock_dict.keys():
        bought_list.append(sym)
    target_buy_count = 3 # 매수할 종목 수
    buy_percent = 0.33 # 종목당 매수 금액 비율
    buy_amount = total_cash * buy_percent  # 종목별 주문 금액 계산
    soldout = False

    send_message("===국내 주식 자동매매 프로그램을 시작합니다===")
    send_message(f"거래상위 10개 종목: {symbol_list}")

    while True:
        t_now = datetime.datetime.now()
        t_9 = t_now.replace(hour=9, minute=0, second=0, microsecond=0)
        t_start = t_now.replace(hour=9, minute=5, second=0, microsecond=0)
        t_sell = t_now.replace(hour=15, minute=15, second=0, microsecond=0)
        t_exit = t_now.replace(hour=15, minute=20, second=0,microsecond=0)
        today = datetime.datetime.today().weekday()

        if today == 5 or today == 6:  # 토요일이나 일요일이면 자동 종료
            send_message("주말이므로 프로그램을 종료합니다.")
            break
        if t_9 < t_now < t_start and soldout == False: # AM 09:00 ~ AM 09:05 : 잔여 수량 매도
            for sym, qty in stock_dict.items():
                sell(sym, qty)
            soldout == True
            bought_list = []
            stock_dict = get_stock_balance()
        # if t_start < t_now < t_sell :  # AM 09:05 ~ PM 03:15: 매수 # default
        t_sell_new = t_now.replace(hour=13, minute=0, second=0, microsecond=0) # added for an improvement on 9/29
        if t_start < t_now < t_sell_new :  # AM 09:05 ~ PM 12:00 : 매수. added for an improvement on 9/29
            for sym in symbol_list:
                if len(bought_list) < target_buy_count:
                    if sym in bought_list:
                        continue
                    target_price = get_target_price(sym)
                    current_price = get_current_price(sym)
                    if target_price < current_price:
                        buy_qty = 0  # 매수할 수량 초기화
                        buy_qty = int(buy_amount // current_price)
                        if buy_qty > 0:
                            send_message(f"{sym} 목표가 달성({target_price} < {current_price}) 매수를 시도합니다.")
                            result = buy(sym, buy_qty)
                            # if len(symbol_list) < 10: # added for an improvement on 11/2
                            #     continue
                            if result:
                                soldout = False
                                bought_list.append(sym)
                                get_stock_balance()
                            # elif (result == False) and ('APBK1680' in {str(res.json())}) : # result == False. added for an improvement on 10/7 str(res.json())
                            #     pass
                            else:
                                continue

                    time.sleep(1)
            time.sleep(1)
            if t_now.minute == 30 and t_now.second <= 5: 
                get_stock_balance()
                time.sleep(5)
        if t_sell < t_now < t_exit:  # PM 03:15 ~ PM 03:20: 일괄 매도
            if soldout == False:
                stock_dict = get_stock_balance()
                for sym, qty in stock_dict.items():
                    sell(sym, qty)
                soldout = True
                bought_list = []
                time.sleep(1)
        if t_exit < t_now:  # PM 03:20 ~ : 프로그램 종료
            send_message("프로그램을 종료합니다.")
            break
        if t_sell_new < t_now < t_sell:
            if len(bought_list) == 0: # 조기 종료. added for an improvement on 10/31
                send_message("매수 시간 내(AM 09:05 ~ PM 12:00)에 조건에 맞는 종목을 매수 할 수 없었으므로, 프로그램을 종료합니다.")
                break

except Exception as e:
    send_message(f"오류 발생!: {e}")
    time.sleep(1)