from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, View
from main.forms import CreateVotingForm, CreateQuestionForm, CreateVariantForm, CreateComplaint
from main.models import Voting, Question, Variant, VoteFact, Complaint
from votings.settings import BASE_URL
import logging


class MainPage(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Main Page',
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        logging.info(f'User {self.request.user} visited main page.')
        return super().render_to_response(context, **response_kwargs)


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        logging.info(f'User {self.object} signed up.')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        logging.error(f'User {self.object} failed to sign up.')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Register',
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        logging.info(f'User {self.request.user} visited sign up page.')
        return super().render_to_response(context, **response_kwargs)


def logout_view(request):
    logout(request)
    logging.info(f'User {request.user} logged out.')
    return redirect('index')


class ListVotingsPage(LoginRequiredMixin, ListView):
    template_name = 'votings/list.html'
    context_object_name = 'votings'
    queryset = Voting.get_active_votings()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({
            'title': 'List Votings',
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        logging.info(f'User {self.request.user} visited list votings page.')
        return super().render_to_response(context, **response_kwargs)


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

    def form_valid(self, form):
        response = super().form_valid(form)
        logging.info(f'User {self.request.user} created voting {self.object}.')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        logging.error(f'User {self.request.user} failed to create voting.')
        return response


class CreateQuestionPage(LoginRequiredMixin, CreateView):
    form_class = CreateQuestionForm
    template_name = 'votings/create_questions.html'

    def get_success_url(self):
        return reverse_lazy('voting', kwargs={'id': self.object.voting.id})

    def get_initial(self):
        voting = get_object_or_404(Voting, id=self.kwargs['id'])
        if voting.author != self.request.user:
            raise PermissionDenied()
        return {
            'voting': voting
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Create Questions',
        })
        return context

    def form_valid(self, form):
        voting = form.instance.voting
        if len(voting.get_questions()) > 0:
            logging.error(f'User {self.request.user} failed to create second question for voting {voting}.')
            raise PermissionDenied()
        response = super().form_valid(form)
        logging.info(f'User {self.request.user} created question {self.object}.')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        logging.error(f'User {self.request.user} failed to create question.')
        return response


class CreateVariantsPage(LoginRequiredMixin, CreateView):
    form_class = CreateVariantForm
    template_name = 'votings/create_variants.html'

    def get_success_url(self):
        return reverse_lazy('question', kwargs={'id': self.object.question.id})

    def get_initial(self):
        question = get_object_or_404(Question, id=self.kwargs['id'])
        if question.voting.author != self.request.user:
            raise PermissionDenied()
        return {
            'question': question
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Create Variants',
        })
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        logging.info(f'User {self.request.user} created variant {self.object}.')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        logging.error(f'User {self.request.user} failed to create variant.')
        return response


class VotingPage(LoginRequiredMixin, TemplateView):
    template_name = 'votings/voting.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Voting',
            'BASE_URL': BASE_URL,
        })
        voting = get_object_or_404(Voting, id=self.kwargs['id'])
        context['voting'] = voting
        context['questions'] = voting.get_questions()
        context['voted'] = voting.is_user_voted(self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        voting = get_object_or_404(Voting, id=self.kwargs['id'])
        if not voting.is_user_voted(request.user):
            keys = request.POST.getlist('variant_id')
            for key in keys:
                variant = get_object_or_404(Variant, id=key)
                VoteFact.vote(request.user, variant)
        return redirect('voting', id=voting.id)

    def render_to_response(self, context, **response_kwargs):
        logging.info(f'User {self.request.user} visited voting {context["voting"]}.')
        return super().render_to_response(context, **response_kwargs)


@login_required()
def publish_voting(request, id: int):
    voting = get_object_or_404(Voting, id=id)
    if voting.author != request.user:
        logging.error(f'User {request.user} failed to publish voting {voting}.')
        raise PermissionDenied()
    voting.publish()
    logging.info(f'User {request.user} published voting {voting}.')
    return redirect('voting', id=voting.id)


class QuestionPage(LoginRequiredMixin, TemplateView):
    template_name = 'votings/question.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Question',
        })
        question = get_object_or_404(Question, id=self.kwargs['id'])
        if question.voting.author != self.request.user:
            raise PermissionDenied()
        context['question'] = question
        context['variants'] = question.get_variants()
        return context

    def render_to_response(self, context, **response_kwargs):
        logging.info(f'User {self.request.user} visited question {context['question']}')
        return super().render_to_response(context, **response_kwargs)


class ProfilePage(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(get_user_model(), id=self.kwargs['id'])
        is_same_user = user == self.request.user
        votings_of_user = Voting.get_votings_of_user(user)
        liked_votings = Voting.get_liked_votings(user)
        voted_votings = Voting.get_voted_votings(user)
        context.update({
            'title': 'Profile',
            'user': user,
            'is_same_user': is_same_user,
            'votings_of_user': votings_of_user,
            'liked_votings': liked_votings,
            'voted_votings': voted_votings,
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        logging.info(f'User {self.request.user} visited {context['user']}\'s profile.')
        return super().render_to_response(context, **response_kwargs)


class ListComplainsPage(UserPassesTestMixin, LoginRequiredMixin, ListView):
    template_name = 'complains/list.html'
    context_object_name = 'complains'
    queryset = Complaint.get_opened_complains()

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({
            'title': 'List Complains',
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        logging.info(f'User {self.request.user} visited complaints page.')
        return super().render_to_response(context, **response_kwargs)


class ComplaintPage(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    template_name = 'complains/complaint.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Complain',
        })
        complain = get_object_or_404(Complaint, id=self.kwargs['id'])
        context['complaint'] = complain
        return context

    def post(self, request, *args, **kwargs):
        complain = get_object_or_404(Complaint, id=self.kwargs['id'])
        key = request.POST.get('result')
        if key == 'skip':
            complain.skip()
        else:
            complain.block()
        return redirect('complains_list')

    def render_to_response(self, context, **response_kwargs):
        logging.info(f'User {self.request.user} visited complaint {context['complaint']}')
        return super().render_to_response(context, **response_kwargs)


class CreateComplaintPage(LoginRequiredMixin, CreateView):
    template_name = 'complains/create_complaint.html'
    form_class = CreateComplaint

    def get_success_url(self):
        return reverse_lazy('voting', kwargs={'id': self.kwargs['id']})

    def get_initial(self):
        voting = get_object_or_404(Voting, id=self.kwargs['id'])
        return {
            'user': self.request.user,
            'voting': voting
        }

    def form_valid(self, form):
        response = super().form_valid(form)
        logging.info(f'User {self.request.user} created complaint {self.object}.')
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        logging.error(f'User {self.request.user} failed to create complaint.')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Create Complaint',
        })
        return context


def like_voting(request, id: int):
    voting = None
    try:
        voting = Voting.objects.get(id=id)
        voting.like(request.user)
        logging.info(f'User {request.user} liked voting {voting}')
    except:
        return JsonResponse({'message': 'Invalid id'}, status=404)
    return JsonResponse({'count likes': voting.get_likes_count()}, status=200)
