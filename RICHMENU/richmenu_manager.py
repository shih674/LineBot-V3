from linebot import (
    LineBotApi
)
from linebot.models import RichMenu


import json

# 讀取重要TOKEN
with open('linebotToken.json', 'r', encoding='utf8') as f:
    content = json.load(f)
line_bot_api = LineBotApi(content['YOUR_CHANNEL_ACCESS_TOKEN'])
print(":: SYSTEM MSG :: line bot TOKEN 載入成功")


# 將設定檔傳給line

# 讀取json檔

# 轉成json格式

# line_bot_api傳給line

# 把rich menu id打印出來
# subject = '閱讀'
# txt_name = subject+'.txt'
# png_name = subject+'.png'
# with open(txt_name, 'r', encoding='utf8') as json_file:
#     rich_menu_json_object = json.load(json_file)
# # 將json格式做成RichMenu的變數
# richMenu = RichMenu.new_from_json_dict(rich_menu_json_object)
# rich_menu_id = line_bot_api.create_rich_menu((richMenu))
# print(rich_menu_id)

# 把照片傳給指定的圖文選單id
rich_menu_id = 'richmenu-5ffd31503c8634eba28e9b63ffb13b3b'
with open('閱讀1.png', 'rb') as image_file:
    response = line_bot_api.set_rich_menu_image(
           rich_menu_id=rich_menu_id,
           content_type='image/jpeg',
           content=image_file
       )
print(response)
print("綁定完成")

# 綁定用戶
#userid = ''
# rich_menu_id = 'richmenu-976c03298edd87b604d0a1eab80b746c'
# line_bot_api.link_rich_menu_to_user(
#    user_id=userid,
#    rich_menu_id=rich_menu_id
# )

# ==========================================================
# 解除綁定
# userid = ''
# line_bot_api.unlink_rich_menu_from_user(
#    user_id=userid
# )

# ===========================================================
# 刪除圖文選單
# while True:
#     rich_menu_id = input('請輸入圖文選單ID  >>')
#     #rich_menu_id = 'richmenu-139bd108a8c5d3c239a76976126ff5d6'
#     line_bot_api.delete_rich_menu(rich_menu_id=rich_menu_id)
#     print(f'已成功刪除圖文選單', rich_menu_id, '\n')
