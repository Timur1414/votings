from lib2to3.fixes.fix_input import context

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from main.forms import CreateVotingForm, CreateQuestionForm, CreateVariantForm
from main.models import Voting, Question


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


class CreateVotingPage(LoginRequiredMixin, CreateView):
    form_class = CreateVotingForm
    template_name = 'votings/create_voting.html'

    def get_success_url(self):
        return reverse_lazy('voting', kwargs={'id': self.object.id})

    def get_initial(self):
        return {
            'author': self.request.user
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Create Voting',
        })
        return context


@login_required()
def create_questions(request, id: int):
    context = {
        'title': 'Create Questions'
    }
    voting = get_object_or_404(Voting, id=id)
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            return redirect('voting', id=voting.id)
    else:
        context['form'] = CreateQuestionForm(initial={'voting': voting})
    return render(request, 'votings/create_questions.html', context)


@login_required()
def create_variants(request, id: int):
    context = {
        'title': 'Create Variants'
    }
    question = get_object_or_404(Question, id=id)
    if request.method == 'POST':
        form = CreateVariantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question', id=question.id)
    else:
        context['form'] = CreateVariantForm(initial={'question': question})
    return render(request, 'votings/create_variants.html', context)


@login_required()
def voting(request, id: int):
    context = {
        'title': 'Voting'
    }
    voting = get_object_or_404(Voting, id=id)
    context['voting'] = voting
    context['questions'] = voting.get_questions()
    return render(request, 'votings/voting.html', context)


@login_required()
def publish_voting(request, id: int):
    voting = get_object_or_404(Voting, id=id)
    voting.publish()
    return redirect('voting', id=voting.id)


@login_required()
def question(request, id: int):
    context = {
        'title': 'Question'
    }
    question = get_object_or_404(Question, id=id)
    context['question'] = question
    context['variants'] = question.get_variants()
    return render(request, 'votings/question.html', context)
