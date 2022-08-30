# <u>주식 자동 매매 패키지</u>

네이버 금융 / Investing.com을 참고하여 거래량 순으로 국내 / 미국 주식 종목코드를 넣어주면,
<br/><br/>
해당 종목들의 주가와 변동성 돌파 전략(Volatility Breakout by Larry Williams)을 기반으로 매수 조건에 맞는지 파악한 뒤
<br/><br/>
한국투자증권 Open API를 활용하여 자동 매매(데이 트레이드)하는 패키지.
<br/><br/>
디스코드 웹훅을 이용하여 장이 설 동안 일정 간격으로 채널 알림(매수 / 매도, 보유 종목, 잔고, 손익)이 오도록 함.

![img](https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTA3MjNfMjk3%2FMDAxNjI3MDM3NjkxMTI0.KkBJouUC9VmPiZsvYHAA4-uL40Fzxuwg9ORT3KVX6pcg.qE6T-aPICOQFNh4LaDXYyc9yd3Gjsm7WbZ3pjmVnvUMg.PNG.kc9994%2Fimage.png&type=sc960_832)

<br/>

## 폴더 구조

├── jeon2_package

│   ├── KoreaStockAutoTrade.py

│   ├── UsaStockAutoTrade.py

│   ├── StockCrawler.py

│   ├── StockAuto.sh

│   ├── StockLog.log

│   ├── config.yaml

│   └── urls.txt

<br/>

## 모듈 설명
- KoreaStockAutoTrade.py: 국내 주식 자동 매매

- UsaStockAutoTrade.py: 미국 주식 자동 매매

- StockCrawler.py: 주식 종목코드 크롤러 on 네이버 금융 by 거래량순

- StockAuto.sh: 부팅 시 crontab으로 .py 모듈들이 자동 실행되는 쉘 스크립트

- StockLog.log: 자동 매매 로그. 매수 / 매도, 보유 종목, 잔고, 손익 기록

- config.yaml: 한국투자증권 Open API key, 디스코드 웹훅 URL 설정 파일

- urls.txt: 웹 크롤링 할 사이트 주소