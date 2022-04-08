import os
import json
import requests
import itertools
from bs4 import BeautifulSoup


class ParseHH:

    def __init__(self, professional_role: list = [], items_on_page: int = 50, page: int = 0):

        self.page = page
        self.items_on_page = items_on_page
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                      ' Chrome/100.0.4896.79 Safari/537.36'}
        self.link = ''
        self.html = ''
        self.soup = ''
        self.prof_role = professional_role

        self.update()

        self.arr_skills = []
        self.max_page = self.soup.find_all('a', {'data-qa': 'pager-page'})[-1].find('span').text

    def update(self):

        prof = ''

        if len(self.prof_role) > 0:
            for item in self.prof_role:
                prof = prof + f'professional_role={item}&'

        self.link = f'https://hh.ru/search/vacancy?{prof}items_on_page={self.items_on_page}&page={self.page}'
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

    def parseVacRes(self, links):
        skills = []

        for link in links:
            r = requests.get(link, headers=self.headers)
            soup = BeautifulSoup(r.text, 'html5lib');

            tags = soup.find_all('span', class_='bloko-tag__section bloko-tag__section_text')
            skill = []
            for tag in tags:
                skill.append(tag.text)

            skills.append(skill)

        return skills


if __name__ == '__main__':

    prof_role = [73, 96, 104, 112, 113, 114, 124, 126]

    parse = ParseHH(prof_role, 50)

    list_titles = []
    list_links = []
    list_skills = []

    for i in range(parse.getMaxPage()):
        parse.page = i
        parse.update()

        t, l = parse.getInfoLinks()
        list_titles.append(t)
        list_links.append(l)
        list_skills.append(parse.parseVacRes(l))

        os.system('cls' if os.name == 'nt' else 'clear')

        print('█' * int(i / parse.getMaxPage() * 100 / 4), end='')
        print(f" | {i}/{parse.getMaxPage()}", end='')
        print(f' {int(i / parse.getMaxPage() * 100)}%')

    data = {
        "titles": list(itertools.chain(*list_titles)),
        "links": list(itertools.chain(*list_links)),
        "skills": list_skills
    }

    with open('data.json', 'w+', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))