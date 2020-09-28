import bs4
import json
import requests
from multiprocessing import Pool
from functools import partial
import urllib3

class Everytime():
    def __init__(self, id=None, pwd=None):
        self._s = requests.Session()
        self._s.headers.update({
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        })
        if id and pwd:
            self.login(id, pwd)

    def __del__(self):
        self._s.close()

    def _get_request(self, url):
        return self._s.get(url)

    def _post_request(self, url, data={}):
        try:
            return self._s.post(url, json.dumps(data))
        except:
            return None

    def _get_article_list(board_id):
        url = 'https://api.everytime.kr/find/board/article/list'

    def login(self, id, password):
        res = self._post_request('https://everytime.kr/user/login', {
            'userid': id,
            'password': password,
            'redirect': '/'
        })
        return not ('history.go(-1)' in res.text)

    def show_board(self, number, start=0):
        res = self._post_request('https://api.everytime.kr/find/board/article/list', {
            'id': number,
            'moiminfo': 'true',
            'start_num': start,
            'limit_num': '20'
        })        # print(soup)
        try:
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            result = {
                'title': soup.find('moim')['name'],
                'articles': [ int(x['id']) for x in soup.find_all('article') ]
            }
        except TypeError or AttributeError:
            result = {
                'title': '',
                'articles': []
            }
        return result 

    def show_article(self, number, comments=False):
        res = self._post_request('https://api.everytime.kr/find/board/comment/list', {
            'id': number,
            'limit_num': -1
        })
        try:
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            res_dict = {
                'title': soup.find('article')['title'],
                'content': soup.find('article')['text']
            }
        except TypeError or AttributeError:
            return {
                'title': '',
                'content': '',
                'comments': []
            }
        if comments:
            res_dict['comments'] = [item['text'] for item in soup.find_all('comment')]
        return res_dict

    def get_list_and_show_articles(self, number, count):
        for i in range(0, count, 20):
            print("count: {}|".format(i))
            ids = self.show_board(number, i)['articles']
            for id in ids: yield self.show_article(id, True)
        # return result

    def get_list_and_show_articles_parallel(self, number, count):
        for i in range(0, count, 20):
            print("count: {}|".format(i))
            ids = self.show_board(number, i)['articles']
            if len(ids) < 1: break
            pool = Pool()
            yield pool.map(partial(self.show_article, comments=True), ids)
            pool.close()



class CampusPick(Everytime):
    def __init__(self, id=None, pwd=None):
        super().__init__(id, pwd)
        self.board_id_dict = {
            738: "개당당한 아싸모임"
        }

    def login(self, id, password):
        res = self._post_request('https://api.campuspick.com/find/login', {
            'userid': id,
            'password': password,
        })
        json_res = json.loads(res.text)
        token = json_res["result"]["token"]
        user_res = self._post_request('https://api.campuspick.com/find/user', {
            'token': token
        })
        return not ('history.go(-1)' in user_res.text)

    def show_board(self, number, before_id=None):
        form = {
            'boardId': number,
        }
        if before_id: form['beforeId'] = before_id
        res = self._post_request('https://api.campuspick.com/find/articles', form)
        try:
            res_dict = json.loads(res.text)      
            return [item["id"] for item in res_dict["result"]["articles"]]
        except json.decoder.JSONDecodeError:
            return 
        
        # print(soup)
        # try:
        #     soup = bs4.BeautifulSoup(res.text, 'json.parser')
        #     result = {
        #         'title': soup.find('moim')['name'],
        #         'articles': [ int(x['id']) for x in soup.find_all('article') ]
        #     }
        # except TypeError or AttributeError:
        #     result = {
        #         'title': '',
        #         'articles': []
        #     }
        # return result 

    def get_board_id(self, display_id):
        res = self._get_request("https://www.campuspick.com/community?id={}".format(display_id))
        try:
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            soup = soup.find('body')
            result = {
                'board_id': soup.find('div', {"id": "container"})['data-board-id']
            }
        except TypeError or AttributeError:
            result = {
                'board_id': -1
            }
        return result 

    def show_article(self, number, comments=False):
        res = self._post_request('https://api.campuspick.com/find/comments', {
            'articleId': number,
        })
        try:
            res_json = json.loads(res.text)
            # print(res_json)
            res_json = res_json["result"] if res_json["status"] == "success" else None
            # raise AttributeError

            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            res_dict = {
                'title': '',
                'content': res_json["article"]["text"]
            }
        except TypeError or AttributeError:
            return {
                'title': '',
                'content': '',
                'comments': []
            }
        except json.decoder.JSONDecodeError:
            return {
                'title': '',
                'content': '',
                'comments': []
            }
        if comments:
            res_dict['comments'] = [item['text'] for item in res_json["comments"]]
            res_dict['article_id'] = number
        return res_dict

    def get_list_and_show_articles_parallel(self, number, count):
        board_id = self.get_board_id(number)['board_id']
        last_idx = None #None 중단되면 이부분에 마지막 id값을 넣어준다.
        for i in range(0, count, 20):
            print("count: {}|".format(i))
            ids = self.show_board(board_id, last_idx)
            if len(ids) < 1: break
            pool = Pool()
            last_idx = ids[-1]
            yield pool.map(partial(self.show_article, comments=True), ids)
            pool.close()


# cp = CampusPick("yaya996", "hwa3991?")
# print(len(cp.show_board(260149)))
