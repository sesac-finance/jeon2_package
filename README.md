# <u>주식 자동 매매 패키지</u>

네이버 금융 / Investing.com에서 거래량 순으로 국내 / 미국 주식 종목코드를 웹크롤러로 가져오면,
<br><br>
해당 종목들의 주가와 변동성 돌파 전략(Volatility Breakout by Larry Williams)을 기반으로 매수 조건에 맞는지 파악한 뒤
<br><br>
한국투자증권 Open API과 Crontab을 활용하여 자동 매매(데이 트레이드)하는 패키지.
<br><br>
디스코드 웹훅을 이용하여 장이 설 동안 일정 간격으로 채널 알림(매수 / 매도, 보유 종목, 잔고, 손익)이 오도록 함.

![img](https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTA3MjNfMjk3%2FMDAxNjI3MDM3NjkxMTI0.KkBJouUC9VmPiZsvYHAA4-uL40Fzxuwg9ORT3KVX6pcg.qE6T-aPICOQFNh4LaDXYyc9yd3Gjsm7WbZ3pjmVnvUMg.PNG.kc9994%2Fimage.png&type=sc960_832)
<br>

<P align='center'><img src="https://github.com/sesac-finance/jeon2_package/blob/master/20220915_%ED%95%9C%ED%88%AC%EC%86%90%EC%9D%B5.jpg?raw=true", width="300" height="600"/> <img src="/mnt/FE0A5E240A5DDA6B/workspace/jeon2_package/20220920_한투손익.jpg" width="300" height="600"/><P>

<br>

## 폴더 구조

├── jeon2_package

│   ├── KoreaStockAutoTrade.py

│   ├── UsaStockAutoTrade.py

│   ├── StockCrawler.py

│   ├── StockCrawler2.ipynb

│   ├── StockAuto.sh

│   ├── StockLog.log

│   ├── config.yaml

│   ├── SkinnyBrownInstagramCrawler.py

│   ├── InstagramConfig.yaml

│   ├── requirements.txt

│   ├── urls.txt

│   └── README.md

<br/>

## 모듈 설명
- KoreaStockAutoTrade.py: 국내 주식 자동 매매

- UsaStockAutoTrade.py: 미국 주식 자동 매매

- StockCrawler.py: 주식 종목코드 크롤러 on 네이버 금융 by 거래량순

- StockCrawler2.ipynb: StockCrawler.py Ver. 2. 추가 데이터 수집 및 시각화 작업 중

- StockAuto.sh: 평일 오전 9시 10분에 crontab으로 국내 주식 자동 매매 모듈이 자동 실행되는 쉘 스크립트

- StockLog.log: 자동 매매 로그. 매수 / 매도, 보유 종목, 잔고, 손익 기록

- config.yaml: 한국투자증권 Open API key, 디스코드 웹훅 URL 설정 파일

- SkinnyBrownInstagramCrawler.py: 번외. 스키니 브라운 인스타그램에서 공연 관련 해시태그가 포함된 최신 게시물만 크롤링

- InstagramConfig.yaml: 번외. 인스타그램 로그인 계정 정보 파일

- requirements.txt: Anaconda 가상환경에 설치된 패키지들 목록

- urls.txt: 웹 크롤링 할 사이트 주소

- README.md: 패키지 설명