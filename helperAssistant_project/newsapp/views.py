from django.shortcuts import render, redirect


# Create your views here.
def news_list(request):
    return render(request, 'newsapp/news.html', {})
