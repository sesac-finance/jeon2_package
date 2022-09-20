"""
<Version 2>
- 신규 메시지 확인: Updater, CommandHandler, start_polling(), idle() 사용
- 봇 종료 불가
"""
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
import telegram
from telegram.ext import Updater, CommandHandler

ig_e = (NoSuchElementException, StaleElementReferenceException,)

# 인스타그램 로그인 계정
with open('/mnt/FE0A5E240A5DDA6B/workspace/jeon2_package/WebCrawler/InstagramConfig.yaml', encoding='UTF-8') as f:
    _cfg = yaml.load(f, Loader=yaml.FullLoader)
username = _cfg['username']
userpw = _cfg['userpw']

# 인스타그램 로그인 URL
loginURL = 'https://www.instagram.com/accounts/login/'

# Chrome Option 추가
# chrome_options = wd.ChromeOptions()
# chrome_options.add_argument('lang=ko_KR')
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--single-process')
# chrome_options.add_argument('window-size=1920,1080')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36')

# Chrome driver 실행
driver = wd.Chrome(service=Service(ChromeDriverManager().install())) # Selenium 4 버전 대 , options=chrome_options
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

# 로그인 정보 나중에 저장하기 클릭하고 넘어가기. XPATH 일부가 매번 바뀌기 때문에 class로 찾아 줌
# try:
elem = WebDriverWait(driver, 10, ignored_exceptions=ig_e)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, '._acan._acao button')))
# except:
#     elem = WebDriverWait(driver, 20, ignored_exceptions=ig_e)\
#         .until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mount_0_0_yP > div > div > div > div.bdao358l.om3e55n1.g4tp4svg > div > div > div > div.alzwoclg.cqf1kptm.p1t2w4gn.fawcizw8.om3e55n1.g4tp4svg > div.bdao358l.cauy2b9r.alzwoclg.cmg2g80i.lk0hwhjd.nfcwbgbd.mivixfar.h4m39qi9.i54nktwv.z2vv26z9.c7y9u1f0.jez8cy9q.cqf1kptm.oq7qnk0t.o9w3sbdw.mx6umkf4.sl27f92c > div.mfclru0v.mdyuua9d.mu7z578c.dx5cv30n.b0g6smra.ixtmsaem > section > main > div > div > div > div > button')))
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

recent3 = []

for a in aTags:
    recent3.append(a.get_attribute('href'))
    
filterTags = ['#콘서트', '#concert', '#CONCERT', '#공연', '#페스티벌', '#festival', '#FESTIVAL', '#라인업', '#lineup', '#LINEUP', '#티켓', '#ticket', '#TICKET', '#사인회']
feed = [] # URL, Tag 딕셔너리 담은 리스트
posts = [] # 모든 포스트(최근 3개)
content = [] # 필요한 태그가 들어가 있는 포스트만

for i in range(3):
    response = requests.get(recent3[i])
    soup = BeautifulSoup(response.text, 'lxml')
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

    driver.get(recent3[i])

    date = WebDriverWait(driver, 10, ignored_exceptions=ig_e)\
    .until(EC.presence_of_element_located((By.TAG_NAME, 'time')))

    date = date.get_attribute('datetime')[:10]

    urltags = f'날짜: {date}, 해시태그: {tags}, URL: {recent3[i]}'
    
    if tags == []:
        continue
    
    feed.append(urltags)
    
# 크롬드라이버 종료
driver.close()

# 텔레그램 시작
telegram_config = {}
with open('/mnt/FE0A5E240A5DDA6B/workspace/practice/RPA/telegram_config', 'r') as f:
    configs = f.readlines()
    for config in configs:
        key, value = config.rstrip().split('=')
        telegram_config[key] = value

token = telegram_config['token']
chat_id = telegram_config['chat_id']
bot = telegram.Bot(token)

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

def add_handler(cmd, func):
    updater.dispatcher.add_handler(CommandHandler(cmd, func))

def start(update, context):
    context.bot.send_message(chat_id, text="봇을 시작합니다.")
 
def stop(update, context):
    context.bot.send_message(chat_id, text="봇을 멈춥니다.")
 
def skinnybrown(update, context):
    if feed:
        context.bot.send_message(chat_id, text=f"공연 관련 해시태그를 포함한 최근 게시물을 보내드려요.\n{str(feed)}")
    
    else:
        context.bot.send_message(chat_id, text="해시태그가 들어간 새로운 게시물이 없어요.")

def newposts(update, context):
    context.bot.send_message(chat_id, text=f"최근 게시물 3개를 보내드려요.\n{str(posts)}")

def tags(update, context):
    context.bot.send_message(chat_id, text=f"공연 관련 해시태그를 보내드려요.\n{str(filterTags)}")

def commands(update, context):
    context.bot.send_message(chat_id, text="안녕하세요! 봇의 명령어를 알려드릴게요. :)")
    context.bot.send_message(chat_id, text="/start: 봇을 시작합니다.")
    context.bot.send_message(chat_id, text="/stop: 봇을 멈춥니다.")
    context.bot.send_message(chat_id, text="/sb: 공연 관련 해시태그를 포함한 최근 게시물이 있는지 알려드려요.")
    context.bot.send_message(chat_id, text="/posts: 최근 게시물 3개를 보내드려요.")
    context.bot.send_message(chat_id, text="/tags: 공연 관련 해시태그를 보내드려요.")

add_handler('start', start)
add_handler('stop', stop)
add_handler('sb', skinnybrown)
add_handler('posts', newposts)
add_handler('tags', tags)
add_handler('command', commands)

updater.start_polling(timeout=3, clean=True)
updater.idle()