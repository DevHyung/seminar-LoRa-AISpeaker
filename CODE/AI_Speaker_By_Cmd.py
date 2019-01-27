# -*- coding: utf-8 -*-
#!/usr/bin/env3 python
# [START import_libraries]
from konlpy.tag import Twitter
import requests

twitter = Twitter()
# [END import_libraries]
'''=================Custom Parameter ======================='''
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:\\Users\\PHJ\\Downloads\\LoRa-d8553681a920.json"
myIp = 'http://192.168.0.145' # INPUT_YOUR_WEMOS_IP

urlList = [
    myIp+'/first_floor_off',
    myIp+'/first_floor_on',
    myIp+'/second_floor_off',
    myIp+'/second_floor_on',
    '분석 실패하여 Log 를 저장합니다.'
]
# 동사 목록
# frame : ['형태소원형','URL weight']
verbList = [
    ['끄다',0],
    ['켜다',1]
]
# 명사 목록
nounList = [
    # 명령어, 대답
    ['위층',2],
    ['윗층',2],
    ['위',2],
    ['아래층',0],
    ['아렛층',0],
    ['밑',0],
]
# 1층 으로 인식될떄의 1에대한 Number 형태소
numberList = [
    ['1',0],
    ['2',2]
]
def getUrl(nounWeight,numberWeight,verbWeight):
    urlResult = -1
    if nounWeight == -1 and numberWeight != -1 and verbWeight != -1:  # 숫자로 말한경우
        urlResult = numberWeight + verbWeight
    elif nounWeight != -1 and numberWeight == -1 and verbWeight != -1:
        urlResult = nounWeight + verbWeight

    return urlResult

def getWeightNoun(dicts):
    print(">>> 명사(Noun )  형태소: ", end='')
    nounWeight = -1
    for d in dicts:
        if d[1] == 'Noun':
            for n in nounList:
                if d[0] == n[0]:
                    nounWeight = n[1]
            print(d, end=',')
    print()
    return nounWeight
def getWeightNumber(dicts):
    print(">>> 숫자(Number) 형태소: ", end='')
    numberWeight = -1
    for d in dicts:
        if d[1] == 'Number':
            print(d, end=',')
            for n in numberList:
                if d[0] == n[0]:
                    numberWeight = n[1]
    print()
    return numberWeight

def getWeightVerb(dicts):
    print(">>> 동사(Verb)   형태소: ", end='')
    verbWeight = -1
    for d in dicts:
        if d[1] == 'Verb':
            print(d, end=',')
            for v in verbList:
                if d[0] == v[0]:
                    verbWeight = v[1]
    print()
    return verbWeight


'''========================================================='''

def CommandProc(stt):
    # 문자 양쪽 공백 제거
    cmd = stt.strip().replace(' ','')
    # 입력 받은 문자 화면에 표시

    #NLP get weight
    dicts = twitter.pos(cmd, norm=True, stem=True)

    print(">>> 전체 형태소        : ",dicts)
    nounWeight = getWeightNoun(dicts)
    numberWeight = getWeightNumber(dicts)
    verbWeight = getWeightVerb(dicts)
    print(">>> Weight 값        : Noun = {}, Number = {}, Verb = {}".
        format(nounWeight, numberWeight, verbWeight))
    urlResult = getUrl(nounWeight,numberWeight,verbWeight)

    # 결과
    print(">>> GET : ",urlList[urlResult])
    try:
        requests.get(urlList[urlResult])
    except:
        pass
    print("___"*30) # 줄 분리

    return 1 # 60초 동안 계속 사용하기위해


if __name__ == '__main__':
    while True:
        cmd = input(">>> 명령어 입력:").strip()
        CommandProc(cmd)