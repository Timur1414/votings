from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView


class MainPage(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Main Page',
        })
        if self.request.user.is_authenticated:
            context['name'] = 'Hello, ' + self.request.user.username
        return context


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Register',
        })
        return context


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required()
def list_votings_page(request):
    context = {
        'title': 'List Votings'
    }
    context['votings'] = []
    return render(request, 'votings/list.html', context)
