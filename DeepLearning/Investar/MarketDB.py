import pandas as pd
#from bs4 import BeautifulSoup
#import urllib
#from urllib.request import urlopen
import pymysql
#import time
#import pandas.io.sql as sql
from datetime import datetime
#from threading import Timer
#import matplotlib.pyplot as plt

class MarketDB:
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""

        self.codes = dict()
        db_config = {} #config 불러오기
        with open('/mnt/FE0A5E240A5DDA6B/workspace/jeon2_package/DeepLearning/Investar/db_config', 'r') as f:
            for l in f.readlines():
                key, value = l.rstrip().split('=')
                if key == 'port':
                    db_config[key] = int(value)
                else:
                    db_config[key] = value
        try:
            self.conn = pymysql.connect(**db_config)
            print("DB 접속 성공")
            
        except Exception as e:
            print(f'접속 실패: {e}')

        self.getCompanyInfo()
        
    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()

    def getCompanyInfo(self):
        """company_info 테이블에서 읽어와서 companyData와 codes에 저장"""
        sql = "SELECT * FROM company_info"
        companyInfo = pd.read_sql(sql, self.conn)
        for idx in range(len(companyInfo)):
            self.codes[companyInfo['code'].values[idx]] = companyInfo['company'].values[idx]

    def getDailyPrice(self, code, startDate, endDate):
        """daily_price 테이블에서 읽어와서 데이터프레임으로 반환"""
        sql = "SELECT * FROM daily_price WHERE code = '{}' and date >= '{}' and date <= '{}'".format(code, startDate, endDate)
        df = pd.read_sql(sql, self.conn)
        df.index = df['date']
        return df