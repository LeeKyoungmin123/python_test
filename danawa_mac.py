# selenium import
from selenium import webdriver
import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# 엑셀처리 임포트
import xlsxwriter
# 이미지 바이트 처리
from io import BytesIO
import urllib.request as req

# 헤더 정보 초기화
opener = req.build_opener()
# User Agent 정보
opener.addheaders = [('User-agent', UserAgent().ie)]
# 헤더 정보 삽입
req.install_opener(opener)

# 엑셀 처리 선언
workbook = xlsxwriter.Workbook(
    "C:/Users/Stephen/Desktop/programming/py1230/danawa_result_apple_macbook.xlsx")

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
browser.get('http://prod.danawa.com/list/?cate=112758&15main_11_02')

# 제조사별 더 보기 클릭1
# Explicitly wait
# WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dlMaker_simple"]/dd/div[2]/button[1]'))).click()

# 제조사별 더 보기 클릭2
# Implicitly wait
time.sleep(3)
browser.find_element_by_xpath(
    '//*[@id="dlMaker_simple"]/dd/div[2]/button[1]').click()


# 원하는 모델 카테고리 클릭
# WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectMaker_simple_priceCompare_A"]/li[12]/label'))).click()
time.sleep(2)
browser.find_element_by_xpath(
    '//*[@id="selectMaker_simple_priceCompare_A"]/li[12]/label').click()
time.sleep(3)

# 현재 페이지
cur_page = 1

# 크롤링 페이지 수
target_crawl_num = 5

# 엑셀 행수
ins_cnt = 1

while cur_page <= target_crawl_num:

    # bs4 초기화
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # 소스코드 정리
    # print(soup.prettify())

    # 메인 상품 리스트 선택
    pro_list = soup.select(
        'div.main_prodlist.main_prodlist_list > ul.product_list > li')

    # 페이지 번호 출력
    print("***** Current Page : {}".format(cur_page), "*****\n")

    # 필요 정보 추출
    for i, v in enumerate(pro_list, 1):

        if not v.find('div', class_='ad_header'):
            prod_name = v.select_one('p.prod_name > a').text.strip()
            # print(prod_name)

            prod_price = v.select_one('p.price_sect > a').text.strip()
            # print(prod_price)

            if v.find('img', class_='image_lazy'):
                prod_img = v.find('img')['data-original']
            else:
                prod_img = v.find('img')['src']

            # print(prod_img)

            # 이미지 바이트 변환처리
            img_data = BytesIO(req.urlopen(prod_img).read())

            # 엑셀에 텍스트 저장
            worksheet.write("A{}".format(ins_cnt), prod_name)
            worksheet.write("B{}".format(ins_cnt), prod_price)

            # 엑셀에 이미지 저장
            worksheet.insert_image("C{}".format(ins_cnt), prod_name, {
                                   'image_data': img_data})

            ins_cnt += 1

        print()
    print()

    # 페이지 별 스크린샷 저장
    # browser.save_screenshot("D:/target_page{}.png".format(cur_page))

    # 페이지 증가
    cur_page += 1

    if cur_page > target_crawl_num:
        print("crawling succeed!")
        break

    # 페이지 이동 클릭
    browser.find_element_by_css_selector(
        'div.number_wrap > a:nth-child({})'.format(cur_page)).click()

    # 3초간 대기
    time.sleep(3)

    # bs4 삭제
    del soup

# 브라우저 종료
browser.close()

workbook.close()
