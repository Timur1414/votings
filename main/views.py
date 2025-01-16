from django.contrib.auth import logout
from django.shortcuts import render, redirect


def main_page(request):
    context = {
        'title': 'Main Page',
        'header': 'Main Page',
    }
    if request.user.is_authenticated:
        context['name'] = 'Hello, ' + request.user.username
    return render(request, 'index/index.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')
