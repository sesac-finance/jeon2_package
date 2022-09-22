import pandas as pd
from pandas_datareader import data as pdr # 데이터 로딩 및 시각화를 위한 라이브러리
import yfinance as yf # 금융 데이터 가져오는 Yahoo Finance
yf.pdr_override() # 둘이 합체!
from scipy import stats # 회귀 분석을 위한 수학, 과학, 엔지니어링용 핵심 패키지 모음(넘파이 기반)
import matplotlib.pylab as plt # 그래프 출력
from datetime import datetime
import os

kospi = pdr.get_data_yahoo('^KS11', '2000-01-04') # KOSPI, 2000-01-04~
today = datetime.now().date() # 오늘 날짜
workspace = os.getcwd() # 현재 작업 경로 확인

# Tickers on Yahoo Finance
symbols = {
    '^DJI': 'DOW Jones Industrial Average',
    'DX-Y.NYB': 'US Dollar Index',
    'KRW=X': 'US Dollar'
}

def Regression(opponent:str='^DJI', filepath:str=workspace): # Regression 함수 선언
    """다우존스 지수/달러 인덱스/달러와 KOSPI 지수 사이의 상관관계를 확인하기 위한 회귀 그래프를 그려주는 함수\n
    opponent='종목 티커', filepath='그래프를 저장할 경로'를 매개변수로 받음"""
    versus = pdr.get_data_yahoo(opponent, '2000-01-04')

    df = pd.DataFrame({'X':versus['Close'], 'Y':kospi['Close']}) # 가로축 독립변수 x: 다우존스 지수, 세로축 종속변수 y: KOSPI 지수
    df = df.fillna(method='bfill') # 뒤의 값으로 결측치 대체
    df = df.fillna(method='ffill') # 마지막 행의 결측치를 앞의 값으로 대체

    regr = stats.linregress(df.X, df.Y) # 선형 회귀 모델 생성
    regr_line = f'Y = {regr.slope:.2f}  X + {regr.intercept:.2f}' # y의 기대치를 나타내는 회귀식. slope: 기울기, intercept: 절편

    plt.figure(figsize=(7, 7)) # 그래프 사이즈
    plt.plot(df.X, df.Y, '.') # X/Y의 좌표를 .으로 찍음 (Scatter Plot, 산점도)
    plt.plot(df.X, regr.slope * df.X + regr.intercept, 'r') # 회귀선을 붉은 선으로 그림
    
    plt.ylabel('KOSPI') # Y축은 KOSPI

    if opponent == '^DJI': # 다우존스 지수와 KOSPI 지수를 비교하고 싶다면
        plt.xlabel(symbols[opponent]) # X축은 DOW
        plt.legend(['DOW x KOSPI', regr_line]) # 범례
        # R 결정계수(상관계수의 제곱): 추정된 회귀선이 변수 사이의 관계를 얼마나 잘 설명하는지. 0 ~ 1
        plt.title(f'DOW x KOSPI (R = {regr.rvalue:.2f})\n2000-01-04 ~ {today}') # 그래프 제목
        plt.savefig(f'{filepath}/DowKospi_Regr.png', format="png", dpi=150) # 그래프 저장. dpi는 해상도

    elif opponent == 'DX-Y.NYB': # 달러 인덱스와 KOSPI 지수를 비교하고 싶다면
        plt.xlabel(symbols[opponent]) # X축은 USDX
        plt.legend(['USDX x KOSPI', regr_line])
        plt.title(f'USDX x KOSPI (R = {regr.rvalue:.2f})\n2000-01-04 ~ {today}')
        plt.savefig(f'{filepath}/USDXKospi_Regr.png', format="png", dpi=150)

    elif opponent == 'KRW=X': # 달러와 KOSPI 지수를 비교하고 싶다면
        plt.xlabel(symbols[opponent]) # X축은 USD
        plt.legend(['USD x KOSPI', regr_line])
        plt.title(f'USD x KOSPI (R = {regr.rvalue:.2f})\n2000-01-04 ~ {today}')
        plt.savefig(f'{filepath}/USDKospi_Regr.png', format="png", dpi=150)

    plt.show() # 그래프 그리기
    print(f'{symbols[opponent]}와 KOSPI의 회귀 그래프를 경로: {filepath}에 저장하였습니다.')