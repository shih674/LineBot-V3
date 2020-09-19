import os
import requests
import json
import main

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, FollowEvent, PostbackEvent,
    TextMessage, TextSendMessage
)


app = Flask(__name__)


# 讀取重要TOKEN
with open('linebotToken.json', 'r', encoding='utf8') as f:
    content = json.load(f)
line_bot_api = LineBotApi(content['YOUR_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(content['YOUR_CHANNEL_SECRET'])
print(":: SYSTEM MSG :: line bot TOKEN 載入成功")

with open('Backend_API_url.txt', 'r', encoding='utf8') as f:
    content = f.read()
backend_url = content
print('::SYSTEM MSG:: 後端API網址載入成功', backend_url)

# 呼叫對話引擎API
def callAPIdialog(json_input={"userId": "test000", "msg": "測試資料"}):
    '''
    # 呼叫推薦服務
    :param json_input:
    :return:
    '''
    print('\n::SYS訊息:: 呼叫對話引擎 \n')
    response = requests.post(backend_url, json=json_input)
    response = response.json()
    print('\n::SYS訊息:: retrun content \n', response)
    print('\n::SYS訊息:: return object type: \n', type(response))
    return response


@app.route("/", methods=['GET'])
def hello():
    print(":: SYSTEM MSG :: 有人透過GET呼叫首頁'/'")
    return '我是LINEBOT V3。看到這個訊息，代表本py檔正常執行'


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 取得使用者輸入的文字訊息
    msg = event.message.text
    # 取得使用者ID
    user_id = event.source.user_id

    if '我選擇的是: ' not in msg:
        # 組合成符合API input格式的字典
        api_par = {"userId": user_id, "msg": msg}
        print(f"api_par: {api_par}")
        # 這邊應該要call API
        pass_par = callAPIdialog(api_par)
        print(f"::賴爸msg:: pss_par=",str(pass_par))
        print(f"data type= {type(pass_par)}")
        # pass_par = dict()
        pass_par['userId'] = user_id
        # pass_par['cur_state'] = msg
        # 把從API拿到的訊息交給main解析成linebot要做的動作
        reply_msg_element = main.main(pass_par)

        # 測試api_par內容
        # reply_msg_element.append(TextSendMessage(text=f'pai_par內容: {str(api_par)}'))
        # print(f"pass_par: {pass_par}")
        line_bot_api.reply_message( event.reply_token, reply_msg_element)
        print('\n====================================================================================\n\n')
    else:
        print('圖文選單發出的訊息:', msg)


@handler.add(PostbackEvent)
def handle_postback_event(event):
    # 取得postback回傳內容
    postback = event.postback.data
    print('觸發POSTBACK事件，POSTBACK資料內容為: ', postback)
    # 取得使用者ID
    user_id = event.source.user_id

    # 組合成符合API input格式的字典
    api_par = {"userId": user_id, "msg": postback}
    print(f"api_par: {api_par}")
    # 這邊應該要call API
    pass_par = callAPIdialog(api_par)
    print(f"::賴爸postback:: pss_par=", str(pass_par))
    print(f"data type= {type(pass_par)}")
    pass_par['userId'] = user_id
    # 把從API拿到的訊息交給main解析成linebot要做的動作
    main.main(pass_par)

    # line_bot_api.reply_message(event.reply_token, reply_msg_element)
    print('====================================================================================\n')

    big_interest = postback.split('_')[0]
    interest = postback.split('_')[1]
    # 使用者在九大類別中選擇了...
    if big_interest == '9question':
        # 選擇了音樂
        if interest == '音樂':
            # 提問、綁定圖文選單-音樂
            rich_menu_id = 'richmenu-0e753f5359f10765c15a72cca90c8325'  # 圖文選單-音樂 id
            line_bot_api.link_rich_menu_to_user(user_id=event.source.user_id, rich_menu_id=rich_menu_id)
            print('綁定圖文選單 - 音樂')
            question1 = f'請問 他/她 喜歡什麼類型的音樂呢 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '運動':
            # 提問、綁定圖文選單-運動
            rich_menu_id = 'richmenu-fffe6997e86a40769e887c86e399d7d7'  # 圖文選單-運動 id
            line_bot_api.link_rich_menu_to_user(user_id=event.source.user_id, rich_menu_id=rich_menu_id)
            print('綁定圖文選單 - 運動')
            question1 = f'請問 他/她 喜歡什麼類型的運動呢 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '影劇':
            # 提問、綁定圖文選單-影劇
            rich_menu_id = 'richmenu-7f34f76e2fa310f7536b2372af9f453b'  # 圖文選單-影劇 id
            line_bot_api.link_rich_menu_to_user(user_id=event.source.user_id, rich_menu_id=rich_menu_id)
            print('綁定圖文選單 - 影劇')
            question1 = f'請問 他/她 喜歡什麼類型的影劇呢 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '旅遊':
            # 提問、綁定圖文選單-旅遊
            rich_menu_id = 'richmenu-daba551c917aa72b6d66687c5107854d'  # 圖文選單-旅遊 id
            line_bot_api.link_rich_menu_to_user(user_id=event.source.user_id, rich_menu_id=rich_menu_id)
            question1 = f'請問 他/她 喜歡什麼類型的旅遊呢 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)
            #print('hello')#,user)

        elif interest == '購物':
            # 提問、綁定圖文選單-購物
            rich_menu_id = 'richmenu-273f9b1702ccde01ed8e75165a4e5cc8'  # 圖文選單-購物 id
            line_bot_api.link_rich_menu_to_user(user_id=event.source.user_id, rich_menu_id=rich_menu_id)
            question1 = f'請問 他/她 購物時喜歡買什麼類型的產品呢 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '閱讀':
            # 提問、綁定圖文選單-閱讀
            rich_menu_id = 'richmenu-5ffd31503c8634eba28e9b63ffb13b3b'  # 圖文選單-閱讀 id
            line_bot_api.link_rich_menu_to_user(user_id=event.source.user_id, rich_menu_id=rich_menu_id)
            print('綁定圖文選單 - 閱讀')
            question1 = f'請問 他/她 喜歡什麼風格的書呢 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '電玩':
            # 提問、綁定圖文選單-電玩
            rich_menu_id = 'richmenu-763ccb0dc0d6ac4fda64b7f98083aeac'  # 圖文選單-電玩 id
            line_bot_api.link_rich_menu_to_user(user_id=event.source.user_id, rich_menu_id=rich_menu_id)
            print('綁定圖文選單 - 運動')
            question1 = f'請問 他/她 都玩什麼類型的電玩呢 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '美食':
            # 提問、綁定圖文選單-美食
            rich_menu_id = 'richmenu-dfdba72ba8eb5f8e2d73268e5e2a92ba'  # 圖文選單-美食 id
            line_bot_api.link_rich_menu_to_user(user_id=event.source.user_id, rich_menu_id=rich_menu_id)
            print('綁定圖文選單 - 美食')
            question1 = f'他/她 最喜歡什麼類型的料理呢 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '其他':
            line_bot_api.unlink_rich_menu_from_user(user_id=event.source.user_id)
            question1 = f'請輸入一樣 他/她 感興趣的人、事或物 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

    # 進入六個興趣分類之 音樂圖文選單
    elif big_interest == '音樂':
        line_bot_api.unlink_rich_menu_from_user(user_id=event.source.user_id)
        if interest == '古典音樂':
            question1 = f'請問您，他最喜歡的古典音樂或樂手為何 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '流行音樂':
            question1 = f'請問您，他最喜歡的流行音樂或樂手為何 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '電音樂曲':
            question1 = f'請問您，他最喜歡的電音舞曲或樂手為何？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '嘻哈饒舌':
            question1 = f'請問您，他最喜歡的饒舌音樂或樂手為何 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)
            # print('hello')#,user)

        elif interest == '獨立樂團':
            question1 = f'請問您，他最喜歡的歌曲或是樂團為何 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '其他':
            question1 = f'請問您，他最喜歡的音樂或樂手為何 ？\n請直接輸入~ '
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)
        # 連線到後端改狀態

    # 進入六個興趣分類之 運動圖文選單
    elif big_interest == '運動':
        line_bot_api.unlink_rich_menu_from_user(user_id=event.source.user_id)
        if interest == '田徑':
            question1 = f'請問您，他最喜歡的田徑項目或選手為何 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '球類':
            question1 = f'請問您，他最喜歡的球類項目或選手為何 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '有氧運動':
            question1 = f'請問您，他最喜歡的有氧運動為何 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '無氧運動':
            question1 = f'請問您，他最喜歡的無氧運動為何 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)
            # print('hello')#,user)

        elif interest == '靜態休閒':
            question1 = f'請問您，他最喜歡的靜態休閒運動為何 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '其他':
            question1 = f'請問您，他最喜歡的運動或體育選手為何 ？\n請直接輸入~ '
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)
        # 連線到後端改狀態

    # 進入六個興趣分類之 影劇圖文選單
    elif big_interest == '影劇':
        line_bot_api.unlink_rich_menu_from_user(user_id=event.source.user_id)
        if interest == '美劇':
            question1 = f'請問您，他/ 她最喜歡的美劇或美國明星 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '日劇':
            question1 = f'請問您，他/ 她最喜歡的日劇或日本明星 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '韓劇':
            question1 = f'請問您，他/ 她最喜歡的韓劇或韓星 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '古裝劇':
            question1 = f'請問您，他/ 她最喜歡的古裝劇或大陸/台灣明星 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)
            # print('hello')#,user)

        elif interest == '動漫':
            question1 = f'請問您，他/ 她最喜歡的動漫或動漫角色 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '其他':
            question1 = f'請問您，他/ 她最喜歡的劇名或明星是誰 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)
        # 連線到後端改狀態

    # 進入六個興趣分類之 旅遊圖文選單
    elif big_interest == '旅遊':
        line_bot_api.unlink_rich_menu_from_user(user_id=event.source.user_id)
        if interest == '國內旅遊':
            question1 = f'請問您，他/ 她最喜歡的國內地區 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '美洲度假':
            question1 = f'請問您，他/ 她最喜歡的美洲地區或國家 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '歐洲漫步':
            question1 = f'請問您，他/ 她最喜歡的歐洲地區或國家 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '東南亞探險':
            question1 = f'請問您，他/ 她最喜歡的東南亞地區或國家 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)
            # print('hello')#,user)

        elif interest == '東北亞遊玩':
            question1 = f'請問您，他/ 她你最喜歡的東北亞地區或國家 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '其他':
            question1 = f'您說他/ 她最喜歡出遊的地方是 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)
        # 連線到後端改狀態

    # 進入六個興趣分類之 購物圖文選單
    elif big_interest == '購物':
        line_bot_api.unlink_rich_menu_from_user(user_id=event.source.user_id)
        if interest == '流行服飾':
            question1 = f'請問您，他/ 她常買的服飾品牌或風格 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '家用實物':
            question1 = f'請問您，他/ 她常買得或曾提起得家用物品 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '精品名牌':
            question1 = f'請問您，他/ 她喜歡的精品品牌 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '電子器具':
            question1 = f'請問您，他/ 她需要的電器或喜歡的電器品牌 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)
            # print('hello')#,user)

        elif interest == '護膚保養':
            question1 = f'請問您，他/ 她喜歡用得化妝保養品或品牌 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '其他':
            question1 = f'那麼請問你 他/ 她最近想買的東西是 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)
        # 連線到後端改狀態

    # 進入六個興趣分類之 閱讀圖文選單
    elif big_interest == '閱讀':
        line_bot_api.unlink_rich_menu_from_user(user_id=event.source.user_id)
        if interest == '旅遊叢書':
            question1 = f'請問您，他/ 她最近在看哪本旅遊的書 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '文學小說':
            question1 = f'請問您，他/ 她你最喜歡的小說 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '商業理財':
            question1 = f'請問您，他/ 她最喜歡的理財書籍或作者 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '語言學習':
            question1 = f'請問您，他/ 她最有興趣的語言是 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '心靈勵志':
            question1 = f'請問您，他/ 她最喜歡的心靈勵志叢書或作者 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '其他':
            question1 = f'那麼請問你 他/ 她會感興趣的書是 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

    # 進入六個興趣分類之 電玩圖文選單
    elif big_interest == '電玩':
        line_bot_api.unlink_rich_menu_from_user(user_id=event.source.user_id)
        if interest == '手機遊戲':
            question1 = f'請問您，他/ 她最喜歡的手機遊戲 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '線上遊戲':
            question1 = f'請問您，他/ 她你最喜歡的線上遊戲 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '掌上型遊戲機':
            question1 = f'請問您，他/ 她最喜歡的掌上型遊戲機 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '家用遊戲機':
            question1 = f'請問您，他/ 她最喜歡的家用遊戲機 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)
            # print('hello')#,user)

        elif interest == '心靈勵志':
            question1 = f'請問您，他/ 她最喜歡的大型單機遊戲 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '其他':
            question1 = f'那麼請問你 他/ 她最近玩過的遊戲是 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

    # 進入六個興趣分類之 美食圖文選單
    elif big_interest == '美食':
        line_bot_api.unlink_rich_menu_from_user(user_id=event.source.user_id)
        if interest == '台式':
            question1 = f'請問您，他/ 她最喜歡的台式菜餚 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '中式':
            question1 = f'請問您，他/ 她最喜歡的中式菜餚 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '西式':
            question1 = f'請問您，他/ 她最喜歡的西式菜餚 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '日式':
            question1 = f'請問您，他/ 她最喜歡的日式食物 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '韓式':
            question1 = f'請問您，他/ 她最喜歡的韓式食物 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

        elif interest == '其他':
            question1 = f'那麼請問你 他/ 她最近著迷於何種美食 ？'
            messages1 = TextSendMessage(text=question1)
            line_bot_api.reply_message(event.reply_token, messages1)

    else :
        big_interest = event.postback.data.split('_')[0]
        interest = event.postback.data.split('_')[1]
        print(f"使用者選擇的興趣為: ", big_interest, interest)



@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    user_name = profile.display_name
    print(user_name)
    welcome_word0 = f'{user_name}，您好(hello)！\n感謝您成為送禮達人的好友！\n\n若不想接收提醒，可以點畫面右上方的選單圖示，然後關閉「提醒」喔。'
    messages0 = TextSendMessage(text=welcome_word0)
    # call api 初始化使用者json檔
    # 組合成符合API input格式的字典
    api_par = {"userId": user_id, "msg": 'RESET USER STATES'}
    print(f"api_par: {api_par}")
    # 這邊應該要call API
    pass_par = callAPIdialog(api_par)
    print(f"::賴爸msg:: pss_par=", str(pass_par))
    print(f"data type= {type(pass_par)}")
    response = main.main(pass_par)
    response = [messages0] + response
    line_bot_api.reply_message(event.reply_token, response)



    line_bot_api.reply_message( event.reply_token, reply_msg_element)

if __name__ == "__main__":
    # for heroku
    # app.run(host='0.0.0.0',port=os.environ['PORT'])

    # for localhost
    app.run(host='0.0.0.0')





