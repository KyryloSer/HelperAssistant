from django.shortcuts import render, redirect
from .utils import get_category, get_news


# Create your views here.
def news_list(request):
    category_dict = get_category()
    news_dict = get_news()
    return render(request, 'newsapp/news.html', {'category_dict': category_dict, 'news_dict': news_dict})
