from selenium import webdriver

import time

from bs4 import BeautifulSoup

import codecs

from datetime import datetime


d = datetime.today()

file_path = 'C:/Users/Stephen/Desktop/programming/py1230/멜론 실시간 차트 1~100위 순위({}년 {}월 {}일 {}:{}).html'.format(
    d.year, d.month, d.day, d.hour, d.minute)


with codecs.open(file_path, mode='w', encoding='utf-8') as f:

    driver = webdriver.Chrome(
        'C:/Users/Stephen/Desktop/programming/py1230/chromedriver.exe')

    driver.get('https://melon.com')

    time.sleep(0.5)

    driver.find_element_by_xpath(
        '//*[@id="gnb_menu"]/ul[1]/li[1]/a/span[2]').click()

    time.sleep(1)

    src = driver.page_source

    soup = BeautifulSoup(src, 'html.parser')

    # print(src)

    music_name = soup.find_all('div', class_='ellipsis rank01')

    # music_artist = soup.find_all('div', {'class': 'rank02'})

    print(music_name)

    # print(music_artist)
