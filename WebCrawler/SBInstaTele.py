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

ig_e = (NoSuchElementException, StaleElementReferenceException,)

# 인스타그램 계정
with open('/mnt/FE0A5E240A5DDA6B/workspace/jeon2_package/WebCrawler/InstagramConfig.yaml', encoding='UTF-8') as f:
    _cfg = yaml.load(f, Loader=yaml.FullLoader)
username = _cfg['username']
userpw = _cfg['userpw']

# 인스타그램 로그인 URL
loginURL = 'https://www.instagram.com/accounts/login/'

# Skinny Brown Instagram URL
skinnyURL = 'https://www.instagram.com/skinnybrownn/'

# Tags
filterTags = ['#콘서트', '#concert', '#CONCERT', '#공연', '#페스티벌', '#festival', '#FESTIVAL', '#라인업', '#lineup', '#LINEUP', '#티켓', '#ticket', '#TICKET', '#사인회']

# 텔레그램 봇
telegram_config = {}
with open('/mnt/FE0A5E240A5DDA6B/workspace/practice/RPA/telegram_config', 'r') as f:
    configs = f.readlines()
    for config in configs:
        key, value = config.rstrip().split('=')
        telegram_config[key] = value

token = telegram_config['token']
chat_id = telegram_config['chat_id']

def SBInsta():
    # Chrome driver 실행
    driver = wd.Chrome(service=Service(ChromeDriverManager().install())) # Selenium 4 버전 대
    driver.get(loginURL)
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
    elem = WebDriverWait(driver, 10, ignored_exceptions=ig_e)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#react-root > section > main > div > div > div > div > button')))
    elem.click()

    # 설정 나중에 하기 클릭하고 넘어가기
    elem = WebDriverWait(driver, 3, ignored_exceptions=ig_e)\
        .until(EC.element_to_be_clickable((By.CLASS_NAME, '_a9--._a9_1'))) # XPATH 일부가 매번 바뀌기 때문에 class로 찾아 줌
    elem.click()

    driver.get(skinnyURL)
    driver.implicitly_wait(3)

    WebDriverWait(driver, 3, ignored_exceptions=ig_e)\
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, '._ac7v._aang a')))

    aTags = driver.find_elements(By.CSS_SELECTOR, '._ac7v._aang a')[:3] # 최근 포스트 URL

    recent6 = []

    for a in aTags:
        recent6.append(a.get_attribute('href'))
        
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

        date = WebDriverWait(driver, 3, ignored_exceptions=ig_e)\
        .until(EC.presence_of_element_located((By.TAG_NAME, 'time')))
        date = date.get_attribute('datetime')[:10]

        urltags = f'날짜: {date}, 해시태그: {tags}, URL: {recent6[i]}'
        
        if tags == []:
            continue
        
        feed.append(urltags)

    # 크롬드라이버 종료
    driver.close()

    return feed


# 텔레그램 시작
def TeleBot():
    bot = telegram.Bot(token)
    feed = list(SBInsta())
    msg = str(*feed)
    bot.send_message(chat_id, text='봇이 작동하기 시작합니다.')
    print('봇이 작동하기 시작합니다. 명령을 다 내린 후에는 봇을 종료해주세요.')

    while True:
        try:
            new_message = bot.getUpdates(offset=last_id)[-1]

            if (new_message.message.text == '스키니브라운') or (new_message.message.text == 'SB') or (new_message.message.text == '스브'):
                bot.send_message(chat_id, text=msg)
                bot.send_message(chat_id, text='봇이 당신의 명령을 기다리고 있어요.')
                last_id = new_message.update_id + 1

            elif (new_message.message.text == '멈춰') or (new_message.message.text == '그만') or (new_message.message.text == 'stop'):
                bot.send_message(chat_id, text='봇을 멈춥니다.')
                last_id = new_message.update_id + 1
                break

        except:
            pass

        time.sleep(2)