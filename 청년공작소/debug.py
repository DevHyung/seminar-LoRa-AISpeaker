# 사용법
# 1. 텔레그램에서 먼저 봇을만들고
# 2. 봇토큰입력
# 3. 봇에게 아무말 한마디라도 걸어주세요 
import requests
import json
# == CONFIG 
TOKEN = '662624250:AAHsOzNuy3o9qws_pJiy3pffo2zn4TfVC0o'
botUrl = "https://api.telegram.org/bot{}/".format(TOKEN)

html = requests.get(botUrl+'getUpdates')
jsonStr = json.loads(html.text)
chatId = jsonStr['result'][0]['message']['chat']['id']
chatUrl = "https://api.telegram.org/bot{}/sendMessage?chat_id={}".format(TOKEN, chatId)

# == Using
if __name__=="__main__":
    while True:
        text = input(">>> 봇에게 보낼말 : ")
        requests.get(chatUrl + '&text='+text)