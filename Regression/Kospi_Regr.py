import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf # 금융 데이터 가져오는 Yahoo Finance
yf.pdr_override()
from scipy import stats # 회귀 분석을 위한 수학, 과학, 엔지니어링용 핵심 패키지 모음(넘파이 기반)
import matplotlib.pylab as plt # 그래프 출력
from datetime import datetime
import os

kospi = pdr.get_data_yahoo('^KS11', '2000-01-04') # KOSPI, 2000-01-04~
today = datetime.now().date() # 오늘 날짜
workspace = os.getcwd() # 현재 작업 경로 확인

symbols = { # Tickers on Yahoo Finance
    '^DJI': 'DOW Jones Industrial Average',
    'DX-Y.NYB': 'US Dollar Index',
    'KRW=X': 'US Dollar'
}

def Regression(opponent:str='^DJI', filepath:str=workspace): # Regression 함수 선언
    versus = pdr.get_data_yahoo(opponent, '2000-01-04')

    df = pd.DataFrame({'X':versus['Close'], 'Y':kospi['Close']}) # 가로축 독립변수 x: 다우존스 지수, 세로축 종속변수 y: KOSPI 지수
    df = df.fillna(method='bfill') # 뒤의 값으로 결측치 대체
    df = df.fillna(method='ffill') # 마지막 행의 결측치를 앞의 값으로 대체

    regr = stats.linregress(df.X, df.Y) # 선형 회귀 모델 생성
    regr_line = f'Y = {regr.slope:.2f}  X + {regr.intercept:.2f}' # y의 기대치를 나타내는 회귀식. slope: 기울기, intercept: 절편

    plt.figure(figsize=(10, 10))
    plt.plot(df.X, df.Y, '.')
    plt.plot(df.X, regr.slope * df.X + regr.intercept, 'r')
    
    plt.ylabel('KOSPI')

    if opponent == '^DJI':
        plt.xlabel(symbols[opponent])
        plt.legend(['DOW x KOSPI', regr_line])
        # R 결정계수(상관계수의 제곱): 추정된 회귀선이 변수 사이의 관계를 얼마나 잘 설명하는지. 0 ~ 1
        plt.title(f'DOW x KOSPI (R = {regr.rvalue:.2f})\n2000-01-04 ~ {today}')
        plt.savefig(f'{filepath}/DowKospi_Regr.png', format="png", dpi=150)

    elif opponent == 'DX-Y.NYB':
        plt.xlabel(symbols[opponent])
        plt.legend(['USDX x KOSPI', regr_line])
        plt.title(f'USDX x KOSPI (R = {regr.rvalue:.2f})\n2000-01-04 ~ {today}')
        plt.savefig(f'{filepath}/USDXKospi_Regr.png', format="png", dpi=150)

    elif opponent == 'KRW=X':
        plt.xlabel(symbols[opponent])
        plt.legend(['USD x KOSPI', regr_line])
        plt.title(f'USD x KOSPI (R = {regr.rvalue:.2f})\n2000-01-04 ~ {today}')
        plt.savefig(f'{filepath}/USDKospi_Regr.png', format="png", dpi=150)

    plt.show()
    print(f'{symbols[opponent]}와 KOSPI의 회귀 그래프를 경로: {filepath}에 저장하였습니다.')