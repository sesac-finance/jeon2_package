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
import time
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

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
# chrome_options.add_argument('--headless') # ***** 최소 옵션
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--single-process') # ***** 최소 옵션
# chrome_options.add_argument('window-size=1920,1080')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36')

chrome_options.add_argument("start-maximized") # open Browser in maximized mode
chrome_options.add_argument("disable-infobars") # disabling infobars
chrome_options.add_argument("--disable-extensions") # disabling extensions
chrome_options.add_argument("--disable-gpu") # applicable to windows os only
chrome_options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems ***** 최소 옵션
chrome_options.add_argument("--no-sandbox") # Bypass OS security model ***** 최소 옵션
chrome_options.add_argument('--remote-debugging-port=9222')

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
# selector도 XPath도 일부가 바뀌어서 안 끌려올 때.. Full XPath를 쓰자!(ft. 형준 강사님)
elem = WebDriverWait(driver, 5, ignored_exceptions=ig_e)\
    .until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/button')))
elem.click()

# 설정 나중에 하기 클릭하고 넘어가기
elem = WebDriverWait(driver, 5, ignored_exceptions=ig_e)\
    .until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')))
elem.click()

skinnyURL = 'https://www.instagram.com/skinnybrownn/' # Skinny Brown Instagram URL
driver.get(skinnyURL)
driver.implicitly_wait(3)

WebDriverWait(driver, 3, ignored_exceptions=ig_e)\
    .until(EC.presence_of_element_located((By.CSS_SELECTOR, '._ac7v._aang a'))) # 첫 줄(최근 포스트 3개)만 가져오기

aTags = driver.find_elements(By.CSS_SELECTOR, '._ac7v._aang a')[:3] # 최근 포스트 URL이 담긴 태그 찾기

recent3 = [url.get_attribute('href') for url in aTags] # 최근 포스트들 URL
filterTags = ['#콘서트', '#concert', '#CONCERT', '#공연', '#페스티벌', '#festival', '#FESTIVAL', '#라인업', '#lineup', '#LINEUP', '#티켓', '#ticket', '#TICKET', '#사인회']
feed = [] # {업로드 날짜, 해당되는 해시태그, URL, 본문}
posts = [] # 모든 포스트(최근 3개)
content = [] # 원하는 태그가 들어가 있는 포스트만

# 게시물에서 가져올 이미지들의 공통 Full XPath
samexpath = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div/'
vid = 'div[1]/div/div/video' # 게시물이 영상일 경우
img = 'div/div[1]/div[1]/img' # 게시물이 사진일 경우
images = [] # 게시물에서 추출한 이미지의 src를 담을 리스트

for i in range(3):
    response = requests.get(recent3[i])
    soup = BeautifulSoup(response.text, 'html.parser')
    text = re.sub('[\t\n\r\f\v]', '', soup.text)
    text = re.sub('Skinny Brown on Instagram: ', '', text)
    text = re.sub('"', '', text)
    posts.append(text) # 게시물에서 본문만 추출 후 담기
    
    tags = []
    
    for f in filterTags: # 해시태그와 게시물의 본문을 대조
        if f in text: # 포함되어 있다면 해당된 태그를 담기
            tags.append(f)
            
            if text not in content: # 본문이 원하는 태그가 포함된 리스트 안에 없다면 추가
                content.append(text)
                
            else: # 있다면 넘어감
                continue
            
        else:
            continue

    driver.get(recent3[i])

    date = WebDriverWait(driver, 10, ignored_exceptions=ig_e)\
    .until(EC.presence_of_element_located((By.TAG_NAME, 'time'))) # 업로드 날짜 추출

    date = date.get_attribute('datetime')[:10]

    try: # 게시물이 영상인 경우도 사진인 경우도 있음
        vidtag = WebDriverWait(driver, 5, ignored_exceptions=ig_e)\
            .until(EC.presence_of_element_located((By.XPATH, samexpath + vid))) # 게시물이 영상일 경우

        imgposter = vidtag.get_attribute('poster')

        images.append(imgposter)

    except:
        imgtag = WebDriverWait(driver, 5, ignored_exceptions=ig_e)\
            .until(EC.presence_of_element_located((By.XPATH, samexpath + img))) # 게시물이 사진일 경우

        imgsrc = imgtag.get_attribute('src')

        images.append(imgsrc) # 게시물에서 추출한 이미지의 src를 담음

    urltags = f'날짜: {date} / 해시태그: {tags} / URL: {recent3[i]} / 본문: {text}'
    
    if tags == []: # 게시물 안에 원하는 해시태그가 없을 경우 다음 게시물로 넘어감
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