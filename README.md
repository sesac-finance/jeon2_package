# <u>주식 자동 매매</u>
네이버 금융 / Investing.com을 참고하여 거래량 순으로 국내 ETF / 미국 주식 종목코드를 넣어주면,
<br/><br/>
해당 종목들의 작일 주가와 변동성 돌파전략을 기반으로 매수 조건에 맞는지 파악한 뒤
<br/><br/>
한국투자증권 Open API를 활용하여 자동 매매(데이 트레이드)하는 패키지.
<br/><br/>
디스코드 웹훅을 이용하여 장이 설 동안 일정 간격으로 채널 알림(매수 / 매도, 보유 종목, 잔고, 손익)이 오도록 함.

<br/><br/>

## 폴더 구조

├── jeon2_package

│   ├── KoreaStockAutoTrade.py

│   ├── UsaStockAutoTrade.py

│   └── config.yaml

<br/><br/>

## 모듈 설명
- KoreaStockAutoTrade.py: 국내 ETF 자동 매매.

- UsaStockAutoTrade.py: 미국 주식 자동 매매.

- config.yaml: 한국투자증권 Open API key, 디스코드 웹훅 URL 설정 파일