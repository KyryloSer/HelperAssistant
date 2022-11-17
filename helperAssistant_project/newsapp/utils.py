from bs4 import BeautifulSoup
import requests
import json

HEADERS = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"
}


def get_articles():
    response = requests.get('https://www.unian.ua/', headers=HEADERS).text
    soup = BeautifulSoup(response, 'lxml')
    articles = soup.find(class_="main-menu__content nano").find_all('a')
    news_dict = {}
    for article in articles:
        title = article.text.strip()
        link = article.get('href')
        if 'unian.ua' in link:
            news_dict[title] = link
    return news_dict


if __name__ == '__main__':
    get_articles()
