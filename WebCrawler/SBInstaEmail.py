import re
import yaml
import requests
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from datetime import datetime

ig_e = (NoSuchElementException, StaleElementReferenceException,)

# 인스타그램 로그인 계정
with open('/mnt/FE0A5E240A5DDA6B/workspace/jeon2_package/WebCrawler/InstagramConfig.yaml', encoding='UTF-8') as f:
    _cfg = yaml.load(f, Loader=yaml.FullLoader)
username = _cfg['username']
userpw = _cfg['userpw']

# 인스타그램 로그인 URL
loginURL = 'https://www.instagram.com/accounts/login/'

# Chrome Option 추가
chrome_options = wd.ChromeOptions()
# chrome_options.add_argument('lang=ko_KR')
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--single-process')
chrome_options.add_argument('window-size=1920,1080')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36')

# Chrome driver 실행
driver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) # Selenium 4 버전 대
driver.get(loginURL)
# user_agent = driver.find_element(By.CSS_SELECTOR, '#user-agent').text # no such element
driver.implicitly_wait(3) # 처음 접속 시 대기(페이지 로딩 끝나면 진행)

# login
elem = WebDriverWait(driver, 3, ignored_exceptions=ig_e)\
    .until(EC.presence_of_element_located((By.NAME, 'username')))
elem.send_keys(username)

elem = WebDriverWait(driver, 3, ignored_exceptions=ig_e)\
    .until(EC.presence_of_element_located((By.NAME, 'password')))
elem.send_keys(userpw)
elem.send_keys(Keys.ENTER)

# 로그인 정보 나중에 저장하기 클릭하고 넘어가기
elem = WebDriverWait(driver, 20, ignored_exceptions=ig_e)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#react-root > section > main > div > div > div > div > button')))
elem.click()

# 설정 나중에 하기 클릭하고 넘어가기
elem = WebDriverWait(driver, 20, ignored_exceptions=ig_e)\
    .until(EC.element_to_be_clickable((By.CLASS_NAME, '_a9--._a9_1')))
elem.click() # XPATH 일부가 매번 바뀌기 때문에 class로 찾아 줌

skinnyURL = 'https://www.instagram.com/skinnybrownn/' # Skinny Brown Instagram URL
driver.get(skinnyURL)
driver.implicitly_wait(3)

WebDriverWait(driver, 3, ignored_exceptions=ig_e)\
    .until(EC.presence_of_element_located((By.CSS_SELECTOR, '._ac7v._aang a')))

aTags = driver.find_elements(By.CSS_SELECTOR, '._ac7v._aang a')[:3] # 최근 포스트 URL

recent6 = []

for a in aTags:
    recent6.append(a.get_attribute('href'))
    
filterTags = ['#콘서트', '#concert', '#CONCERT', '#공연', '#페스티벌', '#festival', '#FESTIVAL', '#라인업', '#lineup', '#LINEUP', '#티켓', '#ticket', '#TICKET', '#사인회']
feed = [] # URL, Tag 딕셔너리 담은 리스트
posts = [] # 모든 포스트(최근 3개)
content = [] # 필요한 태그가 들어가 있는 포스트만

for i in range(3):
    response = requests.get(recent6[i])
    soup = BeautifulSoup(response.text, 'html.parser')
    text = re.sub('[\t\n\r\f\v]', '', soup.text)
    text = re.sub('Skinny Brown on Instagram: ', '', text)
    text = re.sub('"', '', text)
    posts.append(text)
    
    tags = []
    
    for f in filterTags:
        if f in text:
            tags.append(f)
            
            if text not in content:
                content.append(text)
                
            else:
                continue
            
        else:
            continue

    driver.get(recent6[i])

    date = WebDriverWait(driver, 10, ignored_exceptions=ig_e)\
    .until(EC.presence_of_element_located((By.TAG_NAME, 'time')))

    date = date.get_attribute('datetime')[:10]

    urltags = f'날짜: {date} / 해시태그: {tags} / URL: {recent6[i]} / 본문: {text}'
    
    if tags == []:
        continue
    
    feed.append(urltags)
    
# 크롬드라이버 종료
driver.close()

print(feed)

SMTP_SERVER = 'smtp.naver.com'
SMTP_PORT = 465
SMTP_USER = 'qqyun15@naver.com'
SMTP_PASSWORD = open('/mnt/FE0A5E240A5DDA6B/workspace/jeon2_package/WebCrawler/email_config', 'r').read().rstrip()

msg = MIMEMultipart('alternative')

if len(feed) == 0:
    feed = '해시태그가 들어간 새로운 게시물이 없어요!'

contents = f'안녕하세요, 지연! \n \
Skinny Brown 인스타그램 피드를 전달드려요. :) \n\n \
{datetime.now().date()}: \n \
{feed} \n\n \
오늘도 좋은 하루! :D'

msg['From'] = SMTP_USER
msg['To'] = SMTP_USER
msg['Subject'] = 'SB 인스타 피드' # 메일 제목

text = MIMEText(contents)
msg.attach(text)

try:
    smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    smtp.login(SMTP_USER, SMTP_PASSWORD)
    smtp.sendmail(SMTP_USER, [SMTP_USER], msg.as_string())

except Exception as e:
    print(f'에러 발생: {e}')
    pass

finally:
    smtp.close()
    print('인스타 피드 메일 전송 완료')