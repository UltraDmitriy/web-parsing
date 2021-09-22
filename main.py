import csv
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

URL = 'https://cyberleninka.ru/search?q=orm&page=1'
FILE = 'about-ORM.csv'


def get_current_url(current_page):
    current_url = f'https://cyberleninka.ru/search?q=orm&page={current_page}'
    return current_url


def get_html(url):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
    driver.get(url)
    r = driver.page_source
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    paginator = soup.find('ul', {"class": "paginator"})
    if paginator:
        return int(paginator.find_all('li')[-1].get_text())
    else:
        return 1


def get_content(html):
    articles = []

    soup = BeautifulSoup(html, 'html.parser')
    search_results_list = soup.find('ul', {'id': 'search-results'})
    for li in search_results_list.findAll('li'):
        name = li.find('h2', {'class': 'title'})
        link = name.find('a')
        author = li.find('span')
        span_block = li.find('span', {'class': 'span-block'})

        print('Заголовок статьи: ' + name.text)
        print('Ссылка: ' + 'https://cyberleninka.ru' + link['href'])
        print('Авторы статьи: ' + author.text)
        print('Год / Журнал: ' + span_block.text)

        articles.append({
            'title': name.text,
            'link': 'https://cyberleninka.ru' + link['href'],
            'authors': author.text,
            'year-journal': span_block.text,
        })
    return articles


def save_file(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Ссылка', 'Авторы', 'Год/Журнал'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['authors'], item['year-journal']])


def parse():
    html = get_html(URL)
    pages_count = get_pages_count(html)
    articles = []
    for page in range(1, pages_count + 1):
        print(f'Парсинг страницы {page} из {pages_count}...')
        html = get_html(get_current_url(page))
        articles.extend(get_content(html))
    save_file(articles, FILE)
    print(f'В CSV файл записано {len(articles)} статей')
    os.startfile(FILE)


parse()
