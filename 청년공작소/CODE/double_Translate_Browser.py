__author__ = "DevHyung(박형준)"
__maintainer__ = "DevHyung(박형준)"
__email__ = "khuphj@gmail.com"
''' 
    실행전 주의할점 !!!
     1. chromedriver 설치후 코드와 같은 디렉토리안에있는지
     2. 프로그램 종료하시려면 '종료' 를 입력하시면됩니다. 
'''
from selenium import webdriver
if __name__ == "__main__":
    driver1 = webdriver.Chrome('./chromedriver')
    driver2 = webdriver.Chrome('./chromedriver')

    driver1.get('https://translate.google.com/?um=1&ie=UTF-8&hl=ko&client=tw-ob#en/ko/')
    driver2.get('https://papago.naver.com/')
    while True:
        inputStr = input(">>> INPUT : ").strip()
        if inputStr == '종료':
            break
        driver1.find_element_by_xpath('//*[@id="source"]').clear()
        driver1.find_element_by_xpath('//*[@id="source"]').send_keys(inputStr)

        driver2.find_element_by_xpath('//*[@id="txtSource"]').clear()
        driver2.find_element_by_xpath('//*[@id="txtSource"]').send_keys(inputStr)