from django.shortcuts import render, redirect
from .utils import get_articles


# Create your views here.
def news_list(request):
    news_dict = get_articles()
    return render(request, 'newsapp/news.html', {'news_dict': news_dict})
