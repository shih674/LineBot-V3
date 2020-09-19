from linebot import LineBotApi
import json
from linebot.models import (
    TextMessage, TextSendMessage, QuickReplyButton, MessageAction, QuickReply
)


# 讀取重要TOKEN
with open('linebotToken.json', 'r', encoding='utf8') as f:
    content = json.load(f)
line_bot_api = LineBotApi(content['YOUR_CHANNEL_ACCESS_TOKEN'])
print(":: SYSTEM MSG :: line bot TOKEN 載入成功")


def scene1():
    # 場景名: wait_user
    reply = []
    welcome_word1 = "歡迎來到「送禮達人」，我們的目標只有一個，就是為您找出讓人感動的禮物。\n\n我們每次會從不同角度協助您選擇，讓您每次都有不同的驚奇。"
    messages1 = TextSendMessage(text=welcome_word1)
    reply.append(messages1)

    welcome_word2 = "請問您要送誰禮物？"
    messages2 = TextSendMessage(text=welcome_word2)
    reply.append(messages2)
    return reply


def scene1_1():
    # 詢問收禮者性別
    # 場景名: basic_info_1
    reply = []
    question1 = f'請問您要送誰禮物?\n  (對方的名字或常用稱呼) \n  (eg: 爸爸)(eg: 老師)(eg: 王大明)'
    messages1 = TextSendMessage(text=question1)
    reply.append(messages1)
    return reply


def scene1_2(subject):
    # 詢問收禮者性別
    # 場景名: basic_info_2
    reply = []
    question1 = f'請問 {subject} 是 男性♂或是 女性♀? \n(限輸入 男/ 女 eg: 男)'
    messages1 = TextSendMessage(text=question1)
    reply.append(messages1)
    return reply


def scene1_3(subject):
    # 詢問使用者收禮者年齡
    # 場景名: basic_info_3
    reply = []
    question1 = f'請問 {subject} 的年紀是? \n  (限輸入整數 eg: 25)'
    messages1 = TextSendMessage(text=question1)
    reply.append(messages1)
    return reply


def scene1_4(subject):
    # 詢問使用者與收禮者的關係
    # 場景名: basic_info_4
    reply = []
    question1 = f'請問您與 {subject} 的關係是? \n  (eg: 家人、同事、朋友、情侶)'
    messages1 = TextSendMessage(text=question1)
    reply.append(messages1)
    return reply


def scene1_5():
    # 詢問使用者購買禮物預算
    # 場景名: basic_info_5
    reply = []
    question1 = f'請問您的預算上限是多少錢(台幣)? \n  (限輸入整數 eg: 500)'
    messages1 = TextSendMessage(text=question1)
    reply.append(messages1)
    return reply


def Nscene2_1(user_id):
    # 暫時命名為這個，待流程確定後會替代 scene2()
    # 綁定圖文選單 九大問題，需要參數 userid, 圖文選單id
    rich_menu_id = 'richmenu-a3540bbc56327fad398ff7823b69d0af'
    line_bot_api.link_rich_menu_to_user(user_id=user_id, rich_menu_id=rich_menu_id)
    reply = []
    question1 = f'請問您，他對哪個領域最感興趣呢 ？ \n提示: 請收起小鍵盤，使用下方的圖文選單，用點選的就好囉~'
    messages1 = TextSendMessage(text=question1)
    reply.append(messages1)
    return reply

def Nscene2_2(user_id):
    # 暫時命名為這個，待流程確定後會替代 scene2()
    # 綁定圖文選單 六大問題，需要參數 userid, 九大問題的答案, 圖文選單id
    pass

def scene2():
    # 場景名: ask_interest
    reply = []
    ask_interst = "他喜歡什麼音樂？電影？影集？人物？"
    messages0 = TextSendMessage(text=ask_interst)
    reply.append(messages0)
    return reply


def scene3(subject, present_cnt, next_tag):
    # 場景名: first_question
    reply = []
    reply_word = f"好的，我們一起來為 {subject} 挑禮物吧"
    messages0 = TextSendMessage(text=reply_word)
    reply.append(messages0)
    reply_word = f"候選禮物數：{present_cnt}"
    messages1 = TextSendMessage(text=reply_word)
    reply.append(messages1)

    reply_items = []
    reply_word = f"您覺得 {subject} 對 {next_tag} 有興趣嗎？\n有／無（換一題)"
    reply_items.append(QuickReplyButton(action=MessageAction(label="有", text="有")))
    reply_items.append(QuickReplyButton(action=MessageAction(label="無,換一題", text="無")))
    messages2 = TextSendMessage(reply_word, quick_reply=QuickReply(items=reply_items))
    reply.append(messages2)

    return reply


def scene4(subject, next_tag):
    # 場景名: question_loop_False
    reply = []
    reply_items = []
    reply_word = f"您覺得 {subject} 對 {next_tag} 有興趣嗎？有／無（換一題)"
    reply_items.append(QuickReplyButton(action=MessageAction(label="有", text="有")))
    reply_items.append(QuickReplyButton(action=MessageAction(label="無,換一題", text="無")))
    messages2 = TextSendMessage(reply_word, quick_reply=QuickReply(items=reply_items))
    reply.append(messages2)
    return reply


def scene5(subject, present_cnt, next_tag, tags):
    # 場景名: question_loop_True
    reply = []
    str_tags = tags[0]
    if len(tags)>1:
        for i in range(1,len(tags)):
            str_tags = str_tags + "、"+tags[i]
    reply_word = f"他有興趣的元素：{str_tags}\n候選禮物數：{present_cnt}"
    messages0 = TextSendMessage(text=reply_word)
    reply.append(messages0)

    # quick btn
    reply_items = []
    reply_word = f"您覺得 {subject} 對 {next_tag} 有興趣嗎？有／無（換一題)"
    reply_items.append(QuickReplyButton(action=MessageAction(label="有", text="有")))
    reply_items.append(QuickReplyButton(action=MessageAction(label="無,換一題", text="無")))
    messages2 = TextSendMessage(reply_word, quick_reply=QuickReply(items=reply_items))
    reply.append(messages2)

    return reply


def scene6(subject, present_cnt, tags, product_info, thx_word):
    # 場景名: end_conversation
    reply = []

    str_tags = tags[0]
    if len(tags)>1:
        for i in range(1,len(tags)):
            str_tags = str_tags + "、"+tags[i]
    reply_word = f"他有興趣的元素：{str_tags}\n候選禮物數：{present_cnt}"
    messages0 = TextSendMessage(text=reply_word)
    reply.append(messages0)

    show_products = f"以下是我們覺得 {subject} 會喜歡的禮物\n"
    no = 1
    for key in product_info.keys():
        show_products = show_products + str(no) + ". " + key + '\n    ' + product_info[key] + "\n"
        no += 1
    messages1 = TextSendMessage(text=show_products)
    reply.append(messages1)
    messages2 = TextSendMessage(text=thx_word)
    reply.append(messages2)
    messages3 = TextSendMessage(text="當您準備好要挑禮物時，傳個訊息讓我知道吧 >.^")
    reply.append(messages3)
    return reply


def main(response):
    state = response['cur_state']
    print('!!!!!!!!response',response)
    if state == "wait_user":
        return scene1()
    elif state == "basic_info_1":
        return scene1_1()
    elif state == "basic_info_2":
        return scene1_2(response["subject"])
    elif state == "basic_info_3":
        return scene1_3(response["subject"])
    elif state == "basic_info_4":
        return scene1_4(response["subject"])
    elif state == "basic_info_5":
        return scene1_5()

    elif state == "9question":
        return Nscene2_1(response['userId'])
    elif state == "6question":
        return Nscene2_2(response['userId'])
    elif state == "open_question":
        return Nscene2_2(response['userId'])

    elif state == "ask_interest":
        return scene2()

    elif state == "first_question":
        return scene3(response["subject"], response['product_cnt'], response['next_tag'])
    elif state == "question_loop_False":
        return scene4(response["subject"], response['next_tag'])
    elif state == "question_loop_True":
        return scene5(response["subject"], response['product_cnt'], response['next_tag'], response["conds"])
    elif state == "end_conversation":
        return scene6(response["subject"], response['product_cnt'], response["conds"], response["products"], response["thx words"])
    else:
        # 變成回音機器人
        reply = []
        messages0 = TextSendMessage(text='出現錯誤狀態，請回頭檢查機器人')
        reply.append(messages0)
        return reply