# selenium import
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
# 엑셀처리 임포트
import xlsxwriter
# 이미지 바이트 처리
from io import BytesIO
import urllib.request as req
from datetime import datetime

d = datetime.today()

file_path = "C:/Users/Stephen/Desktop/programming/py1230/멜론일간차트순위_{}_{}_{}.xlsx".format(
    d.year, d.month, d.day)

# 헤더 정보 초기화
opener = req.build_opener()
# User Agent 정보
opener.addheaders = [('User-agent', UserAgent().ie)]
# 헤더 정보 삽입
req.install_opener(opener)

# 엑셀 처리 선언
workbook = xlsxwriter.Workbook(file_path)

# 워크 시트
worksheet = workbook.add_worksheet()

# 브라우저 안뜨게하기
chrome_options = Options()
chrome_options.add_argument("--headless")

# 브라우저 설정 - headless 모드
# browser = webdriver.Chrome("d:/py1230/chromedriver.exe", options=chrome_options)

# 브라우저 설정 - 일반 모드
browser = webdriver.Chrome(
    "C:/Users/Stephen/Desktop/programming/py1230/chromedriver.exe")

# 크롬 브라우저 내부 대기
browser.implicitly_wait(5)

# 브라우저 사이즈
browser.set_window_size(1280, 1080)

# 페이지 이동
target_page = 'https://www.melon.com/chart/day/index.htm'
browser.get(target_page)

# 엑셀에 텍스트 저장
cell_format = workbook.add_format(
    {'bold': True, 'font_color': 'red', 'bg_color': 'yellow'})
worksheet.write("A1", '순위', cell_format)
worksheet.write("B1", '썸네일', cell_format)
worksheet.write("C1", '가수', cell_format)
worksheet.write("D1", '앨범제목', cell_format)
worksheet.write("E1", '노래제목', cell_format)

soup = BeautifulSoup(browser.page_source, 'html.parser')

count = 2  # 엑셀 행 수 카운트

for cnt in [50, 100]:

    song_tr_list = soup.select('#lst{}'.format(cnt))

    for song_tr in song_tr_list:

        # 순위 찾기
        rank = song_tr.select_one('div.wrap.t_center').text.strip()
        print(rank)

        # 이미지 찾기
        img_tag = song_tr.select_one('div.wrap > a > img')
        img_url = img_tag['src']
        print("이미지:", img_url)

        # 가수 이름 찾기
        artist_name = song_tr.select_one(
            'div.wrap div.ellipsis.rank02 > a').text.strip()
        print(artist_name)

        # 앨범명 찾기
        album_name = song_tr.select_one(
            'div.wrap div.ellipsis.rank03 > a').text.strip()
        print(album_name)

        # 노래명 찾기
        song_name = song_tr.select_one(
            'div.wrap div.ellipsis.rank01 > span > a').text.strip()
        print(song_name)

        print("=" * 40)

        # 이미지 바이트 변환 처리
        try:
            img_data = BytesIO(req.urlopen(img_url).read())
            # 엑셀에 이미지 저장
            worksheet.insert_image("B{}".format(count), img_url, {
                                   'image_data': img_data, 'x_scale': 0.5, 'y_scale': 0.5})
        except:
            pass

        # 엑셀에 텍스트 저장
        worksheet.write("A{}".format(count), rank)
        worksheet.write("C{}".format(count), artist_name)
        worksheet.write("D{}".format(count), album_name)
        worksheet.write("E{}".format(count), song_name)

        count += 1

del soup
browser.close()
workbook.close()
