import requests
from bs4 import BeautifulSoup

html_resp = requests.get('https://cryptorank.io').text
block = BeautifulSoup(html_resp, 'lxml')
rows = block.find_all('tr', class_='sc-a321a998-0 QrTwc init-scroll')

price_btc = rows[0].findAll('p', class_='sc-b7cd6de0-0 sc-28f598be-1 tEDJi nZrBG')[0].text.strip()
price_eth = rows[1].findAll('p', class_='sc-b7cd6de0-0 sc-28f598be-1 tEDJi nZrBG')[0].text.strip()

ltc_resp = requests.get('https://cryptorank.io/price/litecoin').text
check = BeautifulSoup(ltc_resp, 'lxml')
price_ltc = check.findAll('div', class_='sc-cb748c3-0 cwWsJH')[0].text.strip()
