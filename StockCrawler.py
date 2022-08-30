import requests
from bs4 import BeautifulSoup

URL = 'https://finance.naver.com/sise/sise_quant.nhn'
res = requests.get(URL)
# print(res.status_code)

soup = BeautifulSoup(res.text, 'html.parser')
stocks = soup.select('.type_2 tr')[2:]

codes = []

for stock in stocks:
    try:
        stock_n = stock.select_one('.tltle').text
        price = stock.select_one('.number').text.replace(',', '')
        code = stock.select_one('.tltle').attrs['href'][-6:]

        if (('인버스' not in stock_n) and ('레버리지' not in stock_n)) and (int(price) <= 26000):
            codes.append(code)
        else:
            pass
    except:
        continue
        
    if len(codes) == 5:
        break
        
print(codes)