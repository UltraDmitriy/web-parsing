import requests
from bs4 import BeautifulSoup

URL = 'https://cyberleninka.ru/article/c/computer-and-information-sciences/1'
KEYWORD = 'ORM'


def get_html(url):
    r = requests.get(url)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    # list_articles = soup.find('ul', class_='list')

    titles = soup.find('div', class_='title')

    for title in titles:
        if title.text.count(KEYWORD):
            print(title.text)
        else:
            print('Статей по ключевому слову не найдено')


def parse():
    html = get_html(URL)
    # print(html.status_code)
    get_content(html.text)


parse()
