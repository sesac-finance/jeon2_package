import re
import time
import yaml
import requests
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# 인스타그램 로그인 계정
with open('/mnt/FE0A5E240A5DDA6B/workspace/jeon2_package/InstagramConfig.yaml', encoding='UTF-8') as f:
    _cfg = yaml.load(f, Loader=yaml.FullLoader)
username = _cfg['username']
userpw = _cfg['userpw']

time.sleep(3)

# 인스타그램 로그인 URL
loginURL = 'https://www.instagram.com/accounts/login/'

# Chrome drvier 실행
driver = wd.Chrome("/mnt/FE0A5E240A5DDA6B/workspace/practice/chromedriver")
driver.get(loginURL)
time.sleep(3)

# login
driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(username)
driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(userpw)

driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button').click()
time.sleep(3)

# 정보 나중에 저장하기 클릭하고 넘어가기
driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button').click()
time.sleep(3)

# 설정 나중에 하기 클릭하고 넘어가기
driver.find_element(By.CLASS_NAME, '_a9--._a9_1').click() # XPATH 일부가 매번 바뀌기 때문에 class로 찾아 줌
time.sleep(3)

skinnyURL = 'https://www.instagram.com/skinnybrownn/' # Skinny Brown Instagram URL
driver.get(skinnyURL)
time.sleep(3)

aTags = driver.find_elements(By.CSS_SELECTOR, '._ac7v._aang a') # 최근 포스트 URL
time.sleep(3)

hrefs = []

for a in aTags:
    hrefs.append(a.get_attribute('href'))
    
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
    time.sleep(3)

    date = driver.find_element(By.CSS_SELECTOR, '._a9z6._a9za time')
    date = date.get_attribute('datetime')[:10]
    
    urltags = f'날짜: {date}, 해시태그: {tags}, URL: {recent6[i]}'
    
    if tags == []:
        continue
    
    feed.append(urltags)
    
# 크롬드라이버 종료
driver.close()

feed