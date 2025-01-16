from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class MainPage(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Main Page',
            'header': 'Main Page',
        })
        if self.request.user.is_authenticated:
            context['name'] = 'Hello, ' + self.request.user.username
        return context


def logout_view(request):
    logout(request)
    return redirect('index')
