import pickle
import datetime
import requests
from django.shortcuts import render, redirect
from .utils import get_news
from .scraper.scraper.spiders.fuel_parser import file, main as fuel_parser

category_dict = {'Війна в Україні': 'news_war', 'Україна': 'news_society',
                 'Світ': 'news_world', 'Політика': 'news_politics', 'Наука': 'news_science',
                 'Технології': 'news_techno',
                 'Погода': 'news_weather', 'Ціни на паливо': 'news_fuel',
                 'Курси валют': 'news_currency'}

category_routes = {'Війна в Україні': 'https://www.unian.ua/war', 'Україна': 'https://www.unian.ua/society',
                   'Світ': 'https://www.unian.ua/world', 'Політика': 'https://www.unian.ua/politics',
                   'Наука': 'https://www.unian.ua/science', 'Технології': 'https://www.unian.ua/techno'}


# Create your views here.
def news_main(request):
    news_content = get_news()
    return render(request, 'newsapp/news.html', {'category_dict': category_dict, 'news_content': news_content})


def news_war(request):
    source = category_routes.get('Війна в Україні')
    news_content = get_news(source)
    return render(request, 'newsapp/news.html', {'category_dict': category_dict, 'news_content': news_content})


def news_society(request):
    source = category_routes.get('Україна')
    news_content = get_news(source)
    return render(request, 'newsapp/news.html', {'category_dict': category_dict, 'news_content': news_content})


def news_world(request):
    source = category_routes.get('Світ')
    news_content = get_news(source)
    return render(request, 'newsapp/news.html', {'category_dict': category_dict, 'news_content': news_content})


def news_politics(request):
    source = category_routes.get('Політика')
    news_content = get_news(source)
    return render(request, 'newsapp/news.html', {'category_dict': category_dict, 'news_content': news_content})


def news_science(request):
    source = category_routes.get('Наука')
    news_content = get_news(source)
    return render(request, 'newsapp/news.html', {'category_dict': category_dict, 'news_content': news_content})


def news_techno(request):
    source = category_routes.get('Технології')
    news_content = get_news(source)
    return render(request, 'newsapp/news.html', {'category_dict': category_dict, 'news_content': news_content})


def news_weather(request):
    pass
    return render(request, 'newsapp/weather.html')


def news_fuel(request):
    with open(file, 'rb') as fh:
        data = pickle.load(fh)
    return render(request, 'newsapp/fuel.html', {'category_dict': category_dict, "data": data})


def news_currency(request):
    response_api = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5')
    exchange_rate = response_api.json()
    current_date_dt = datetime.date.today()
    current_date = current_date_dt.strftime('%d.%m.%Y')
    return render(request, 'newsapp/currency.html', {'category_dict': category_dict, 'exchange_rate': exchange_rate,
                                                     'current_date': current_date})
