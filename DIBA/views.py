from django.shortcuts import render


def home_page(request):
    context = {
        'data': 'new data'
    }
    return render(request, 'home.html', context)
