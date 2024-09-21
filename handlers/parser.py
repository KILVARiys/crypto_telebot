import requests
from bs4 import BeautifulSoup

def get_crypto_price(coins):
    result = {}
    html_resp = requests.get('https://cryptorank.io/ru').text
    block = BeautifulSoup(html_resp, 'lxml')
    rows = block.find_all('tr', class_='sc-a321a998-0 QrTwc init-scroll')