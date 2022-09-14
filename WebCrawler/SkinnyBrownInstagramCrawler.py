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


ig_e = (NoSuchElementException, StaleElementReferenceException,)

# 인스타그램 로그인 계정
with open('./InstagramConfig.yaml', encoding='UTF-8') as f:
    _cfg = yaml.load(f, Loader=yaml.FullLoader)
username = _cfg['username']
userpw = _cfg['userpw']

# 인스타그램 로그인 URL
loginURL = 'https://www.instagram.com/accounts/login/'

# Chrome driver 실행
driver = wd.Chrome(service=Service(ChromeDriverManager().install())) # Selenium 4 버전 대
driver.implicitly_wait(3) # 처음 접속 시 대기(페이지 로딩 끝나면 진행)
driver.get(loginURL)

WebDriverWait(driver, 3, ignored_exceptions=ig_e)\
    .until(EC.presence_of_element_located((By.NAME, 'username')))

# login
driver.find_element(By.NAME, 'username').send_keys(username)
driver.find_element(By.NAME, 'password').send_keys(userpw)
driver.find_element(By.NAME, 'password').send_keys(Keys.ENTER)

# 로그인 정보 나중에 저장하기 클릭하고 넘어가기
WebDriverWait(driver, 3, ignored_exceptions=ig_e)\
    .until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button')))

driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button').click()

# 설정 나중에 하기 클릭하고 넘어가기
WebDriverWait(driver, 3, ignored_exceptions=ig_e)\
    .until(EC.presence_of_element_located((By.CLASS_NAME, '_a9--._a9_1')))

driver.find_element(By.CLASS_NAME, '_a9--._a9_1').click() # XPATH 일부가 매번 바뀌기 때문에 class로 찾아 줌
# driver.find_elements(By.TAG_NAME, 'button')[?].click()

skinnyURL = 'https://www.instagram.com/skinnybrownn/' # Skinny Brown Instagram URL
driver.implicitly_wait(3)
driver.get(skinnyURL)

WebDriverWait(driver, 3, ignored_exceptions=ig_e)\
    .until(EC.presence_of_element_located((By.CSS_SELECTOR, '._ac7v._aang a')))

aTags = driver.find_elements(By.CSS_SELECTOR, '._ac7v._aang a')[:6] # 최근 포스트 URL

recent6 = []

for a in aTags:
    recent6.append(a.get_attribute('href'))
    
filterTags = ['#콘서트', '#concert', '#CONCERT', '#공연', '#페스티벌', '#festival', '#FESTIVAL', '#라인업', '#lineup', '#LINEUP', '#티켓', '#ticket', '#TICKET', '#사인회']
feed = [] # URL, Tag 딕셔너리 담은 리스트
posts = [] # 모든 포스트(최근 6개)
content = [] # 필요한 태그가 들어가 있는 포스트만

for i in range(6):
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

    WebDriverWait(driver, 3, ignored_exceptions=ig_e)\
    .until(EC.presence_of_element_located((By.TAG_NAME, 'time')))

    date = driver.find_element(By.TAG_NAME, 'time')
    date = date.get_attribute('datetime')[:10]
    
    urltags = f'날짜: {date}, 해시태그: {tags}, URL: {recent6[i]}'
    
    if tags == []:
        continue
    
    feed.append(urltags)
    
# 크롬드라이버 종료
driver.close()

print(feed, content, sep = '\n')