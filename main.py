import os
import json
import requests
import itertools
from bs4 import BeautifulSoup


def maxPage():
    max_page = 0


class ParseHH:

    def __init__(self, professional_role: list = [], items_on_page: int = 50, page: int = 0):

        self.page = page
        self.items_on_page = items_on_page
        self.link = f'https://hh.ru/search/vacancy?&items_on_page={self.items_on_page}&page={self.page}'
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                      ' Chrome/100.0.4896.79 Safari/537.36'}
        self.html = self.getHTML()
        self.soup = BeautifulSoup(self.html, 'html5lib')

        self.arr_skills = []
        self.max_page = self.soup.find_all('a', {'data-qa': 'pager-page'})[-1].find('span').text

    def update(self):
        self.link = f'https://hh.ru/search/vacancy?&items_on_page={self.items_on_page}&page={self.page}'
        self.html = self.getHTML()
        self.soup = BeautifulSoup(self.html, 'html5lib')

    def getMaxPage(self):
        return int(self.max_page)

    def getHTML(self):
        r = requests.get(self.link, headers=self.headers)
        print(r)
        if r.status_code // 100 != 2:
            raise Exception('Link is not valid')

        return r.text

    def getInfoLinks(self):
        titles = self.soup.find_all('a', {'data-qa': 'vacancy-serp__vacancy-title'})

        arr_title = []
        arr_links = []
        for title in titles:
            arr_title.append(title.text)

        for link in titles:
            arr_links.append(link.get('href'))

        return arr_title, arr_links


if __name__ == '__main__':
    parse = ParseHH([], 50)

    list_titles = []
    list_links = []

    for i in range(parse.getMaxPage()):
        parse.page = i
        parse.update()

        t, l = parse.getInfoLinks()
        list_titles.append(t)
        list_links.append(l)

        os.system('cls' if os.name == 'nt' else 'clear')

        print('█' * int(i / parse.getMaxPage() * 100 / 4), end='')
        print(f" | {i}/{parse.getMaxPage()}", end='')
        print(f' {int(i / parse.getMaxPage() * 100)}%')

    data = {
        "titles": list(itertools.chain(*list_titles)),
        "links": list(itertools.chain(*list_links))
    }

    with open('data.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
