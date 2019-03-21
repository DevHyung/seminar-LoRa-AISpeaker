__author__ = "DevHyung(박형준)"
__maintainer__ = "DevHyung(박형준)"
__email__ = "khuphj@gmail.com"
''' 
    실행전 주의할점 !!!
     1. chromedriver 설치후 코드와 같은 디렉토리안에있는지
'''

from selenium import webdriver
from bs4 import BeautifulSoup
import time

if __name__ == "__main__":
    pageIdx = 1
    driver = webdriver.Chrome('./chromedriver')
    driver.get('http://www.lotto.co.kr/article/list/AC01')

    while True:
        driver.execute_script('javascript:paging.goPage({});'.format(pageIdx))
        pageIdx += 1
        bs = BeautifulSoup(driver.page_source,'lxml')
        try:
            ul = bs.find('ul',class_='wnr_cur_list')
            lis = ul.find_all("li")
            for li in lis:
                imgs = li.find_all("img")
                noList = []
                for img in imgs:
                    try:
                        no = img['src'].split('/')[-1].split('.')[0]
                        noList.append(no)
                    except:
                        noList.append('+')
                print(noList)
        except: # 아무것도없는경우
            break
