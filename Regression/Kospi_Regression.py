import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
from scipy import stats
import matplotlib.pylab as plt

kospi = pdr.get_data_yahoo('^KS11', '2000-01-04') # KOSPI, 2000-01-04~

symbols = { # Tickers on Yahoo Finance
    'DOW Jones Industrial Average': '^DJI',
    'US Dollar Index': 'DX-Y.NYB',
    'US Dollar': 'KRW=X'
}

def Regression(opponent:str='^DJI'):
    dow = pdr.get_data_yahoo(opponent, '2000-01-04')

    df = pd.DataFrame({'X':dow['Close'], 'Y':kospi['Close']}) # 가로축 독립변수 x: 다우존스 지수, 세로축 종속변수 y: KOSPI 지수
    df = df.fillna(method='bfill') # 뒤의 값으로 결측치 대체
    df = df.fillna(method='ffill') # 마지막 행의 결측치를 앞의 값으로 대체

    regr = stats.linregress(df.X, df.Y) # 선형 회귀 모델 생성
    regr_line = f'Y = {regr.slope:.2f}  X + {regr.intercept:.2f}' # y의 기대치를 나타내는 회귀식. slope: 기울기, intercept: 절편

    plt.figure(figsize=(10, 10))
    plt.plot(df.X, df.Y, '.')
    plt.plot(df.X, regr.slope * df.X + regr.intercept, 'r')
    
    plt.ylabel('KOSPI')

    if opponent == '^DJI':
        plt.xlabel(symbols[0].keys())
        plt.legend(['DOW x KOSPI', regr_line])
        # R 결정계수(상관계수의 제곱): 추정된 회귀선이 변수 사이의 관계를 얼마나 잘 설명하는지. 0 ~ 1
        plt.title(f'DOW x KOSPI (R = {regr.rvalue:.2f})')
        plt.savefig('/mnt/FE0A5E240A5DDA6B/workspace/DowKospi_Regression.png', format="png", dpi=300)

    elif opponent == 'DX-Y.NYB':
        plt.xlabel(symbols[1].keys())
        plt.legend(['USDX x KOSPI', regr_line])
        plt.title(f'USDX x KOSPI (R = {regr.rvalue:.2f})')
        plt.savefig('/mnt/FE0A5E240A5DDA6B/workspace/USDXKospi_Regression.png', format="png", dpi=300)

    elif opponent == 'KRW=X':
        plt.xlabel(symbols[2].keys())
        plt.legend(['USD x KOSPI', regr_line])
        plt.title(f'USD x KOSPI (R = {regr.rvalue:.2f})')
        plt.savefig('/mnt/FE0A5E240A5DDA6B/workspace/USDKospi_Regression.png', format="png", dpi=300)

    plt.show()