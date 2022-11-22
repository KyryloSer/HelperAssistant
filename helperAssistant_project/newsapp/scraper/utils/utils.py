from bs4 import BeautifulSoup
import requests
import json

HEADERS = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"
}


def get_category():
    response = requests.get('https://www.unian.ua/', headers=HEADERS).text
    soup = BeautifulSoup(response, 'lxml')
    articles = soup.find(class_="main-menu__content nano").find_all('a')
    category_dict = {}
    for article in articles:
        title = article.text.strip()
        link = article.get('href')
        if 'unian.ua' in link:
            category_dict[title] = link
    return category_dict


def get_news(source='https://www.unian.ua/') -> list[dict]:
    response = requests.get(source, headers=HEADERS).text
    soup = BeautifulSoup(response, 'lxml')
    news_list = soup.find(class_="newsfeed__list").find_all('a')
    news_content = []
    for news in news_list:
        try:
            news_dict = {}
            title = news.text.strip()
            if 20 < len(title) < 200:
                if title.startswith('оновлено'):
                    title = title.replace('оновлено', '')
                news_dict['title'] = title
                link = news.get('href')
                response = requests.get(link, headers=HEADERS).text
                soup = BeautifulSoup(response, 'lxml')
                article = soup.find('div', class_="article-text").find_all('p')
                content = ''
                for art in article:
                    content += art.text.strip() + '\n'
                news_dict['content'] = content.strip()
                time_ = soup.find('div', class_="article__info-item")
                time_created = time_.text.strip()
                news_dict['time_created'] = time_created
                news_content.append(news_dict)
        except Exception as err:
            print(f'[ERROR] {err}')
    return news_content


if __name__ == '__main__':
    # get_articles()
    get_news()
