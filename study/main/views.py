from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("<h4>Проверка работы</h4>")

def about(request):
	return HttpResponse("<h4>О нас</h4>")

def store(request):
    context = {
        'title': 'Django server is alive!',  # Пример динамических данных
        # Другие данные, которые вы хотите передать в шаблон
    }
    return render(request, 'main/layout.html', context)
