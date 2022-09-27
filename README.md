# <u>주식 자동 매매 & 인스타그램 피드 패키지</u>

네이버 금융에서 거래량 순으로 국내 주식 종목코드를 웹크롤러로 가져오면,
<br><br>
해당 종목들의 주가와 변동성 돌파 전략(Volatility Breakout by Larry Williams)을 기반으로 매수 조건에 해당하는지 파악한 뒤
<br><br>
한국투자증권 Open API, Lambda, Eventbridge를 활용하여 자동 매매(데이 트레이드)하는 패키지.
<br><br>
디스코드 웹훅을 이용하여 장이 설 동안 일정 간격으로 채널 알림(매수 / 매도, 보유 종목, 잔고, 손익)이 오도록 함.
<br><br>
또한 Skinny Brown 인스타그램에서 웹 크롤링으로 공연과 관련된 해시태그가 담긴 게시물만 가져와 이메일/텔레그램(챗봇)으로 피드 보냄.
<br><br>

![img](https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTA3MjNfMjk3%2FMDAxNjI3MDM3NjkxMTI0.KkBJouUC9VmPiZsvYHAA4-uL40Fzxuwg9ORT3KVX6pcg.qE6T-aPICOQFNh4LaDXYyc9yd3Gjsm7WbZ3pjmVnvUMg.PNG.kc9994%2Fimage.png&type=sc960_832)
<br>

<P align='center'><img src="https://github.com/sesac-finance/jeon2_package/blob/master/TradeModule/20220915_%ED%95%9C%ED%88%AC%EC%86%90%EC%9D%B5.jpg?raw=true", width="300" height="600"/> <img src="https://github.com/sesac-finance/jeon2_package/blob/master/TradeModule/20220920_%ED%95%9C%ED%88%AC%EC%86%90%EC%9D%B5.jpg?raw=true" width="300" height="600"/><P>
<br>

## 폴더 구조
📦jeon2_package  
 ┣ 📂Analyze  
 ┃ ┣ 📂CandleCharts  
 ┃ ┃ ┗ 📜kyc_CandleChart.jpg  
 ┃ ┣ 📂Regression  
 ┃ ┃ ┣ 📜DowKospi_Regr.png  
 ┃ ┃ ┣ 📜KospiRegr.py  
 ┃ ┃ ┣ 📜USDKospi_Regr.png  
 ┃ ┃ ┗ 📜USDXKospi_Regr.png  
 ┃ ┗ 📜StockData.ipynb  
 ┣ 📂DeepLearning  
 ┃ ┣ 📂Investar  
 ┃ ┃ ┣ 📜Analyzer.py  
 ┃ ┃ ┣ 📜DBUpdater.py  
 ┃ ┃ ┣ 📜MarketDB.py  
 ┃ ┃ ┣ 📜config.json  
 ┃ ┃ ┗ 📜db_config  
 ┃ ┗ 📜RNN.ipynb  
 ┣ 📂Docker  
 ┃ ┣ 📜Dockerfile  
 ┃ ┣ 📜KoreaStockAutoTrade.py  
 ┃ ┣ 📜config.yaml  
 ┃ ┗ 📜docker-compose.yml  
 ┣ 📂Font  
 ┃ ┗ 📜hana.ttf  
 ┣ 📂TradeModule  
 ┃ ┣ 📜20220915_한투손익.jpg  
 ┃ ┣ 📜20220920_한투손익.jpg  
 ┃ ┣ 📜KoreaStockAutoTrade.py  
 ┃ ┣ 📜StockAuto.sh  
 ┃ ┣ 📜StockLog.log  
 ┃ ┣ 📜UsaStockAutoTrade.py  
 ┃ ┗ 📜config.yaml  
 ┣ 📂WebCrawler  
 ┃ ┣ 📂Instagram  
 ┃ ┃ ┣ 📂CSV  
 ┃ ┃ ┃ ┗ 📜2022-09-22.csv  
 ┃ ┃ ┣ 📂Configs  
 ┃ ┃ ┃ ┣ 📜InstagramConfig.yaml  
 ┃ ┃ ┃ ┣ 📜email_config  
 ┃ ┃ ┃ ┗ 📜telegram_config  
 ┃ ┃ ┣ 📂Images  
 ┃ ┃ ┃ ┣ 📜2022-09-16-SBInsta.jpg  
 ┃ ┃ ┃ ┣ 📜2022-09-18-SBInsta.jpg  
 ┃ ┃ ┃ ┗ 📜2022-09-19-SBInsta.jpg  
 ┃ ┃ ┣ 📂RPA  
 ┃ ┃ ┃ ┣ 📜SBInstaEmail.log  
 ┃ ┃ ┃ ┗ 📜SBInstaEmail.sh  
 ┃ ┃ ┣ 📜SBInstaEmail.py  
 ┃ ┃ ┣ 📜SBInstaTeleVer1.py  
 ┃ ┃ ┗ 📜SBInstaTeleVer2.py  
 ┃ ┗ 📜StockCrawler.py  
 ┣ 📜.gitignore  
 ┣ 📜README.md  
 ┣ 📜ToDos.txt  
 ┣ 📜jeon2tree.txt  
 ┣ 📜requirements.txt  
 ┗ 📜urls.txt  
18 directories, 52 files

## 모듈 설명

< 주식 >

- KoreaStockAutoTrade.py: 국내 주식 자동 매매

- UsaStockAutoTrade.py: 미국 주식 자동 매매

- StockCrawler.py: 주식 종목코드 크롤러 on 네이버 금융 by 거래량순

- StockAuto.sh: : Crontab 스케줄러 작동 위해 대상과 필요한 명령을 기재해놓은 쉘 스크립트. 주식 자동매매 용

- StockLog.log: Crontab 스케줄러는 대상이 백그라운드에서 돎. 추후 디버깅 시 확인하기 위해 실행할 때마다 업데이트 되는 작동 기록. 주식 자동매매 용

- Dockerfile: 주식 자동 매매 패키지 배포를 위해 도커 이미지 안에 들어갈 내용을 기재해놓은 도커 파일

- config.yaml: 한국투자증권 Open API key, 디스코드 웹훅 URL 설정 파일

- hana.ttf: matplotlib으로 그래프 그릴 때 쓰려고 담아둔 한글 폰트

<br>

< 인스타그램 >

- SBInstaEmail.py:  스키니 브라운 인스타그램에서 공연 관련 해시태그가 포함된 최신 게시물 3개만 크롤링 후, 게시물 내용과 이를 담은 CSV, 이미지들을 첨부파일로 담아 이메일로 전송

- SBInstaTeleVer1.py: 스키니 브라운 인스타그램에서 공연 관련 해시태그가 포함된 최신 게시물 3개만 크롤링 후, 명령어에 해당되는 내용을 텔레그램 메시지로 전송. 종료 조건은 While-Break

- SBInstaTeleVer2.py: 스키니 브라운 인스타그램에서 공연 관련 해시태그가 포함된 최신 게시물 3개만 크롤링 후, 명령어에 해당되는 내용을 텔레그램 메시지로 전송. 종료 조건은 updater.idle()이나 최신 메시지 풀링을 멈추지 않음

- SBInstaEmail.sh: Crontab 스케줄러 작동 위해 대상과 필요한 명령을 기재해놓은 쉘 스크립트. 인스타 웹 크롤링 용

- SBInstaEmail.log: Crontab 스케줄러는 대상이 백그라운드에서 돎. 추후 디버깅 시 확인하기 위해 실행할 때마다 업데이트 되는 작동 기록. 인스타 웹 크롤링 용

- InstagramConfig.yaml: 인스타그램 계정 정보

- telegram_config: 텔레그램 계정 정보

- email_config: 이메일 계정 정보

<br>

< 금융 데이터 분석 >

- StockData.ipynb: 네이버 금융에서 거래량 순으로 가져온 주식 정보를 가지고 분석 및 시각화 한 내용

- KospiRegr.py: 다우존스 지수/달러 인덱스/달러와 KOSPI 지수 사이의 상관관계를 확인하기 위한 회귀 그래프를 그려주는 함수. 매개변수로 종목 티커, 그래프를 저장할 경로를 받음

- CandleCharts: 네이버 금융에서 거래량 순으로 가져온 주식 정보를 가지고 시각화 한 캔들 차트

<br>

< 딥러닝 > * 작업 중: Pandas DataFrame을 DB로 밀어주는 과정에서 SQLAlchemy 충돌

- RNN.ipynb: RDS에 주기적으로 쌓는 주식 데이터로 주가 예측 w/h RNN(recurrent neural network, 순환신경망)

- DBUpdater.py: 네이버 금융의 일별 주식 시세를 매일 웹 크롤링으로 가져와 RDS에 자동 업데이트 하는 모듈

- MarketDB.py: RDS에 구축한 주식 시세를 종목 코드나 기업명으로 조회하게 해주는 API

- Analyzer.py: RDS에 구축한 주식 시세를 종목 코드나 기업명으로 조회하게 해주는 API. + 매개변수로 조회 기간 부여

- config.json: 검색할 일별 시세의 페이지 수가 담긴 설정 파일

- db_config: RDS 계정 정보

<br>

< 기타 >

- ToDos.txt: 프로젝트 진행 상황

- urls.txt: 웹 크롤링 할 사이트 주소

- README.md: 패키지 설명

- requirements.txt: Anaconda 가상환경에 설치된 패키지들 목록

- jeon2tree.txt: 프로젝트 파일 트리

- SeSACProject_JiyeonLee.odp: 프로젝트 PPT 발표자료