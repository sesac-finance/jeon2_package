"""
<Version 1>
- 신규 메시지 확인: bot.get_updates(), message.text 사용
- 반복문으로 '멈춰' 혹은 '그만'이라는 명령에 봇 종료 가능
"""
import re
import time
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

ig_e = (NoSuchElementException, StaleElementReferenceException,)

# 인스타그램 로그인 계정
with open('/mnt/FE0A5E240A5DDA6B/workspace/jeon2_package/WebCrawler/Instagram/Configs/InstagramConfig.yaml', encoding='UTF-8') as f:
    _cfg = yaml.load(f, Loader=yaml.FullLoader)
username = _cfg['username']
userpw = _cfg['userpw']

# 인스타그램 로그인 URL
loginURL = 'https://www.instagram.com/accounts/login/'

# Chrome Option 추가
chrome_options = wd.ChromeOptions()
chrome_options.add_argument("--incognito") # 시크릿 모드
chrome_options.add_argument("--no-sandbox") # Bypass OS security model ***** 최소 옵션
chrome_options.add_argument("--lang=ko_KR") # 한국어 설정
chrome_options.add_argument("--start-maximized") # open Browser in maximized mode
chrome_options.add_argument("--disable-infobars") # disabling infobars
chrome_options.add_argument("--disable-extensions") # disabling extensions
chrome_options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems. 메모리가 부족해서 에러가 발생하는 것을 막아줌 ***** 최소 옵션
chrome_options.add_argument("--disable-setuid-sandbox") # 크롬 드라이버에 setuid를 하지 않음으로써 크롬의 충돌을 막아줌
chrome_options.add_argument("--remote-debugging-port=9222") # 실행된 크롬창을 사용하도록 지정 (원격 디버깅 설정)
chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36") # 사람인 척 하기
# chrome_options.add_argument("--headless") # GUI 디스플레이가 없을 때 혹은 크롤링 팝업 뜨기 원치 않을 때 사용 ***** 최소 옵션
# chrome_options.add_argument('--single-process') # 단일 프로세스로 다중 탭 방지***** 최소 옵션. 하지만 SessionNotCreatedException 발생시키는 원흉! :(

# Chrome driver 실행
driver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) # Selenium 4 버전 대
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
# selector도 XPath도 일부가 바뀌어서 안 끌려올 때.. Full XPath를 쓰자!
try:
    elem = WebDriverWait(driver, 5, ignored_exceptions=ig_e)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mount_0_0_PR > div > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div > div.x78zum5.xdt5ytf.x10cihs4.x1t2pt76.x1n2onr6.x1ja2u2z > div.x9f619.xnz67gz.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.xh8yej3.x1gryazu.x10o80wk.x14k21rp.x1porb0y.x17snn68.x6osk4m > section > main > div > div > div > div > button')))
except:
    elem = WebDriverWait(driver, 5, ignored_exceptions=ig_e)\
        .until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/button')))
elem.click()

# 설정 나중에 하기 클릭하고 넘어가기
elem = WebDriverWait(driver, 5, ignored_exceptions=ig_e)\
    .until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')))
elem.click()

skinnyURL = 'https://www.instagram.com/skinnybrownn/' # Skinny Brown Instagram URL
driver.get(skinnyURL)
driver.implicitly_wait(3)

WebDriverWait(driver, 3, ignored_exceptions=ig_e)\
    .until(EC.presence_of_element_located((By.CSS_SELECTOR, '._ac7v._aang a'))) # 첫 줄(최근 포스트 3개)만 가져오기. '._ac7v._aang a'   

aTags = driver.find_elements(By.CSS_SELECTOR, '._ac7v._aang a')[:3] # 최근 포스트 URL이 담긴 태그 찾기
    
recent3 = [url.get_attribute('href') for url in aTags] # 최근 포스트들 URL
filterTags = ['#콘서트', '#concert', '#CONCERT', '#공연', '#페스티벌', '#festival', '#FESTIVAL', '#라인업', '#lineup', '#LINEUP', '#티켓', '#ticket', '#TICKET', '#사인회']
feed = [] # {업로드 날짜, 해당되는 해시태그, URL, 본문}
posts = [] # 모든 포스트(최근 3개)
content = [] # 원하는 태그가 들어가 있는 포스트만

# 게시물에서 가져올 이미지들의 공통 Full XPath
samexpath = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[1]/div/'
vid = 'div/div/div/div/div/div/div/div/div[1]/img' # 게시물이 영상일 경우
img = 'div[1]/div[2]/div/div/div/ul/li[3]/div/div/div/div/div[1]/img' # 게시물이 사진일 경우
imguploaded = [] # 게시물의 게시일을 담을 리스트. for dict_keys
images = [] # 게시물에서 추출한 이미지의 src를 담을 리스트. for dict_values

for i in range(3):
    response = requests.get(recent3[i])
    soup = BeautifulSoup(response.text, 'lxml') # html.parser
    text = re.sub('[\t\n\r\f\v]', '', soup.text)
    text = re.sub('Skinny Brown on Instagram: ', '', text) # ASH ISLAND on Instagram
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
    .until(EC.presence_of_element_located((By.TAG_NAME, 'time'))) # 업로드 일시 추출

    date = date.get_attribute('datetime')[:10] #태그 속성에서 %Y-%m-%d만 추출

    imguploaded.append(date) # 게시일 담기

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

# 웹 크롤링 끝

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
updates = bot.get_updates()
last_id = updates[-1].update_id

bot.send_message(chat_id, text='봇이 작동하기 시작합니다.')
print('봇이 작동하기 시작합니다. 명령을 다 내린 후에는 봇을 종료해주세요.')

while True:
    try:
        new_message = bot.getUpdates(offset=last_id)[-1]
        command = new_message.message.text
        print(command)
        
        if feed: # 해시태그가 들어간 새로운 게시물 O
            if (command == 'SB') or (command == '스브'): # feed
                for f in feed:
                    bot.send_message(chat_id, text=str(f))
                bot.send_message(chat_id, text='봇이 당신의 명령을 기다리고 있어요.')

            elif (command == '내용'): # content
                for c in content:
                    bot.send_message(chat_id, text=str(c))
                bot.send_message(chat_id, text='봇이 당신의 명령을 기다리고 있어요.')

            elif (command == '최근'): # posts
                for post in posts:
                    bot.send_message(chat_id, text=str(post))
                bot.send_message(chat_id, text='봇이 당신의 명령을 기다리고 있어요.')

            elif (command == '태그'): # filterTags
                bot.send_message(chat_id, text=str(filterTags))
                bot.send_message(chat_id, text='봇이 당신의 명령을 기다리고 있어요.')

            elif (command == '멈춰') or (command == '그만'):
                bot.send_message(chat_id, text='봇을 멈춥니다.')
                break

        else: # 해시태그가 들어간 새로운 게시물 X
            if (command == '최근'):
                for post in posts:
                    bot.send_message(chat_id, text=str(post))                

            elif (command == '태그'):
                bot.send_message(chat_id, text=str(filterTags))               

            elif (command == '멈춰') or (command == '그만'):
                bot.send_message(chat_id, text='봇을 멈춥니다.')
                break
            
            bot.send_message(chat_id, text='해시태그가 들어간 새로운 게시물이 없어요!')

        last_id = new_message.update_id + 1

    except:
        pass

    time.sleep(2)