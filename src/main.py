# -*- coding: utf-8 -*-

import json
import os
import re
import settings
import threading
import time
from everytime import Everytime, CampusPick
# from telegrambot import TelegramBot

boards = []
keywords = []
last = {}

# def load_datas():
#     global boards
#     global keywords

#     if not os.path.isfile('datas.json'):
#         return

#     f = open('datas.json', 'r', encoding='utf8')
#     datas = json.loads(f.read())
#     f.close()

#     boards = datas['boards']
#     keywords = datas['keywords']

# def save_datas():
#     f = open('datas.json', 'w', encoding='utf8')
#     f.write(json.dumps({ 'boards': boards, 'keywords': keywords }))
#     f.close()

# def get_article_info_with_keywords(number):
#     result = et.show_article(number)
#     target = (result['title'] + result['content']).lower()
#     target = re.sub(re.compile('<a.*>'), '', target)

#     return {
#         'title': result['title'],
#         'content': result['content'],
#         'keywords': [ x for x in keywords if x in target ]
#     }

# def core():
#     try:
#         article_group = []
#         article_list = []

#         for board in boards:
#             result = et.show_board(board)

#             if not board in last:
#                 last[board] = { 'title': result['title'], 'last_article': result['articles'][0] }
#                 continue

#             for article in result['articles']:
#                 if article <= last[board]['last_article']:
#                     continue

#                 article_info = get_article_info_with_keywords(article)

#                 if len(article_info['keywords']) == 0:
#                     continue

#                 article_list.append('* https://everytime.kr/%d/v/%d - [%s]' % (board, article, ', '.join(article_info['keywords'])))
#                 time.sleep(2)

#             if len(article_list) > 0:
#                 article_group.append('%s (%d)\n%s' % (last[board]['title'], board, '\n'.join(article_list)))
#                 article_list.clear()

#             last[board]['last_article'] = result['articles'][0]
#             time.sleep(2)

#         if len(article_group) == 0:
#             return

#         message =  '[ 키워드가 감지되었습니다. ]\n'
#         message += '\n'
#         message += '\n\n'.join(article_group)

#         tb.send_message(message)

#     except Exception as e:
#         tb.send_message(str(e))

# def loop():
#     while True:
#         core()
#         time.sleep(60)

# def handle_help(update, context):
#     message =  '/help - 명령어 확인\n'
#     message += '/add [board | keyword] <value> - 게시판 또는 키워드 추가\n'
#     message += '/remove [board | keyword] <value> - 게시판 또는 키워드 삭제\n'
#     message += '/show - 추가된 목록 확인'

#     update.message.reply_text(message)

# def handle_add(update, context):
#     try:
#         if context.args[0] == 'board':
#             board = int(context.args[1])

#             if board in boards:
#                 update.message.reply_text('해당 게시판이 이미 존재합니다.')
#             else:
#                 update.message.reply_text('게시판이 정상적으로 추가되었습니다.')
#                 boards.append(board)
#                 save_datas()

#         elif context.args[0] == 'keyword':
#             keyword = context.args[1].lower()

#             if keyword in keywords:
#                 update.message.reply_text('해당 키워드가 이미 존재합니다.')
#             else:
#                 update.message.reply_text('키워드가 정상적으로 추가되었습니다.')
#                 keywords.append(keyword)
#                 keywords.sort()
#                 save_datas()

#         else:
#             update.message.reply_text('/add [board | keyword] <value> - 게시판 또는 키워드 추가')
#     except:
#         update.message.reply_text('/add [board | keyword] <value> - 게시판 또는 키워드 추가')

# def handle_remove(update, context):
#     try:
#         if context.args[0] == 'board':
#             board = int(context.args[1])

#             if board in boards:
#                 update.message.reply_text('게시판이 정상적으로 제거되었습니다.')
#                 boards.remove(board)
#                 del last[board]
#                 save_datas()
#             else:
#                 update.message.reply_text('해당 게시판이 존재하지 않습니다.')

#         elif context.args[0] == 'keyword':
#             keyword = context.args[1].lower()

#             if keyword in keywords:
#                 update.message.reply_text('키워드가 정상적으로 제거되었습니다.')
#                 keywords.remove(keyword)
#                 save_datas()
#             else:
#                 update.message.reply_text('해당 키워드가 존재하지 않습니다.')

#         else:
#             update.message.reply_text('/remove [board | keyword] <value> - 게시판 또는 키워드 삭제')
#     except:
#         update.message.reply_text('/remove [board | keyword] <value> - 게시판 또는 키워드 삭제')

# def handle_show(update, context):
#     for board in boards:
#         if board in last:
#             continue

#         result = et.show_board(board)
#         last[board] = { 'title': result['title'], 'last_article': result['articles'][0] }

#     message =  '현재 설정된 게시판 목록\n'
#     message += '* ' + '\n* '.join([ '%s (%s) / last: %d' % (last[x]['title'], x, last[x]['last_article']) for x in last ])
#     message += '\n\n'
#     message += '현재 설정된 키워드 목록\n'
#     message += '[ ' + ', '.join(keywords) + ' ]'

#     update.message.reply_text(message)

def load_json(file_path):
    try:
        f = open(file_path, "r")
    except FileNotFoundError:
        f = open(file_path, "w")
        f.write("{\"posts\":[]}")
        f.close()
        f = open(file_path, "r")
    return json.load(f)

def save(json_data, results):
    # json_data = {}
    # try:
    #     f = open(file_path, "r")
    # except FileNotFoundError:
    #     f = open(file_path, "w")
    #     f.write("{\"posts\":[]}")
    #     f.close()
    #     f = open(file_path, "r")

    # # with open(file_path, "r") as json_file:
    # json_data = json.load(f)

    for result in results:
        json_data['posts'].append(result)
    with open(file_path, 'w', encoding='utf-8') as outfile:
        json.dump(json_data, outfile, indent=4, ensure_ascii=False)


class EverytimeJsonData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.json_data = self._load_json()

    def _load_json(self):
        try:
            f = open(self.file_path, "r")
        except FileNotFoundError:
            f = open(self.file_path, "w")
            f.write("{\"posts\":[]}")
            f.close()
            f = open(self.file_path, "r")
        return json.load(f)

    def save(self, results):
        # json_data = {}
        # try:
        #     f = open(file_path, "r")
        # except FileNotFoundError:
        #     f = open(file_path, "w")
        #     f.write("{\"posts\":[]}")
        #     f.close()
        #     f = open(file_path, "r")

        # # with open(file_path, "r") as json_file:
        # json_data = json.load(f)

        for result in results:
            self.json_data['posts'].append(result)
        with open(self.file_path, 'w', encoding='utf-8') as outfile:
            json.dump(self.json_data, outfile, indent=4, ensure_ascii=False)
    

def main():
    if not et.login(settings.everytime['id'], settings.everytime['password']):
        print('로그인 실패! 아이디와 비밀번호를 확인해 주세요.')
        return

    # data = et.get_list_and_show_articles_parallel(settings.everytime["board"], 300000)
    articles_per_shard = 50000
    shard = 0
    cnt = 0
    json_data = EverytimeJsonData('{}{}.json'.format(settings.saved["file_name"], shard))
    for sh_data in et.get_list_and_show_articles_parallel(settings.everytime["board"], 300000):
        if cnt >= articles_per_shard:
            cnt = 0
            shard += 1
            json_data = EverytimeJsonData('{}{0:03d}.json'.format(settings.saved["file_name"], shard))
        json_data.save(sh_data)
        cnt += 20

if __name__ == '__main__':
    et = CampusPick() #Everytime()
    # tb = TelegramBot(settings.telegram_bot['token'], settings.telegram_bot['chat_id'])

    # Start
    main()
