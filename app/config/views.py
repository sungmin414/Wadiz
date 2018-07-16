from django.shortcuts import render


def index(request):
    # TEMPLATE 설정 app/template 추
    return render(request, 'index.html')
