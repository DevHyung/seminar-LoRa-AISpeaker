# 사용법
# 1. 텔레그램에서 먼저 봇을만들고
# 2. 봇토큰입력
# 3. 봇에게 아무말 한마디라도 걸어주세요 
import requests
import json
# == CONFIG 
TOKEN = 'INPUT_YOUR_TOKEN' 
botUrl = "https://api.telegram.org/bot{}/".format(TOKEN)

html = requests.get(Bot_URL+'getUpdates')
jsonStr = json.loads(html.text)
chat_id = jsonStr['result'][0]['message']['chat']['id']
chat_url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}".format(TOKEN, chat_id)

# == Using
if __name__=="__main__":
    while True:
        _text = input(">>> 봇에게 보낼말 : ")
        requests.get(chat_url + '&text='+_text)