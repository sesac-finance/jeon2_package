"""
<Version 2>
- 신규 메시지 확인: Updater, CommandHandler, start_polling(), idle() 사용
- Ctrl + c로 봇 종료 불가
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
samexpath = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[1]/div/div/'
vid = 'div[1]/div/div/video' # 게시물이 영상일 경우
img = 'div/div[1]/div[1]/img' # 게시물이 사진일 경우
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
with open('/mnt/FE0A5E240A5DDA6B/workspace/jeon2_package/WebCrawler/Instagram/Configs/telegram_config', 'r') as f:
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
    context.bot.send_message(chat_id, text="Ctrl + c 단축키로 봇을 멈출 수 있다는데.. 습(SB)봇이 지금은 가고 싶지 않데요!")

# feed = [1, 2, 3] # 피드가 있는 경우, 봇의 답변을 확인하기 위해서 임의로 부여

def skinnybrown(update, context):
    if feed:
        context.bot.send_message(chat_id, text=f"공연 관련 해시태그를 포함한 최근 게시물을 보여드려요.\n\n") # {str(feed)}
        for f in feed:
            context.bot.send_message(chat_id, f)
    
    else:
        context.bot.send_message(chat_id, text="해시태그가 들어간 새로운 게시물이 없어요.")

def newposts(update, context):
    context.bot.send_message(chat_id, text=f"최근 게시물 3개의 본문을 보여드려요.\n\n") # {str(posts)}
    for p in posts:
        context.bot.send_message(chat_id, p)


# Ver. 1: 로컬에 저장된 이미지 보내기
# imgpath = '/mnt/FE0A5E240A5DDA6B/workspace/jeon2_package/WebCrawler/Instagram/Images/'

# attachimgs = os.listdir(imgpath) # 첨부파일들 담을 리스트 작업 시작
# attachments = []

# for attachimg in attachimgs: # 경로가 다른 사진들 각각에 절대경로 부여
#     target_img = imgpath + attachimg
#     attachments.append(target_img)

def sendimgs(update, context):
    context.bot.send_message(chat_id, text=f"최근 게시물 3개의 사진을 보여드려요.\n\n")
    for im in images:
        context.bot.send_photo(chat_id, im) # Ver. 1: URL로 이미지 보내기

    # Ver. 1
    # image_file1 = open(attachments[0], 'rb')
    # image_file2 = open(attachments[1], 'rb')
    # image_file3 = open(attachments[2], 'rb')
    # context.bot.send_photo(chat_id, image_file1)
    # context.bot.send_photo(chat_id, image_file2)
    # context.bot.send_photo(chat_id, image_file3)

def showtags(update, context):
    context.bot.send_message(chat_id, text=f"크롤링 타겟인 공연 관련 해시태그를 보여드려요.\n\n{str(filterTags)}")

def commands(update, context):
    context.bot.send_message(chat_id, text="안녕하세요! 습(SB)봇 명령어를 알려드릴게요. :)\n\n/start: 습(SB)봇을 시작합니다.\n/stop: Ctrl + c 단축키로 습(SB)봇을 멈출 수 있어요.\n/sb: 공연 관련 해시태그를 포함한 최근 게시물이 있는지 알려드려요.\n/posts: 최근 게시물 3개의 본문을 보여드려요.\n/images: 최근 게시물 3개의 사진을 보여드려요.\n/tags: 크롤링 타겟인 공연 관련 해시태그를 보여드려요.")

add_handler('start', start)
add_handler('stop', stop)
add_handler('sb', skinnybrown)
add_handler('posts', newposts)
add_handler('tags', showtags)
add_handler('images', sendimgs)
add_handler('commands', commands)

updater.start_polling(timeout=3, clean=True)
updater.idle() # Ctrl + c로 봇 (polling) 중지. 작동 안 하는 듯..