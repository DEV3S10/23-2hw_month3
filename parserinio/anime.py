import requests
from bs4 import BeautifulSoup as bs

URL = 'https://rezka.ag/animation/'

HEADERS = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}


def get_html(url, params=''):
    req = requests.get(url=url, headers=HEADERS, params=params)
    return req


def get_data(html):
    soup = bs(html, 'html.parser')
    items = soup.find_all('div', class_='b-content__inline_item')
    animes = []
    for i in items:
        info = i.find('div', class_="b-content__inline_item-link").find('div').string.split(', ')
        anime = {
            'title': i.find('div', class_="b-content__inline_item-link").find('a').string,
            'link': i.find('div', class_="b-content__inline_item-link").find('a').get('href'),
            'status': i.find("span", class_='info').string
            if i.find("span", class_='info') is not None else "Full screen",
        }

        try:
            anime['year'] = info[0]
            anime['country'] = info[1]
            anime['genre'] = info[2]
        except IndexError:
            anime['year'] = info[0]
            anime['country'] = "Unknown creator"
            anime['genre'] = info[1]

        animes.append(anime)
    return animes


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        animes = []
        for i in range(1, 70):
            html = get_html(f"{URL}page/{i}/")
            current_page = get_data(html.text)
            animes.extend(current_page)
        return animes
    else:
        raise Exception("Error in parser!")
