from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView

from main.models import Voting


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


class ListVotingsPage(LoginRequiredMixin, ListView):
    template_name = 'votings/list.html'
    context_object_name = 'votings'
    queryset = Voting.objects.filter(blocked=False).all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({
            'title': 'List Votings',
        })
        return context
