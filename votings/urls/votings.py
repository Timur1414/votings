from django.urls import path
from main import views

urlpatterns = [
    path('list/', views.ListVotingsPage.as_view(), name='list_votings'),
    path('create_voting/', views.CreateVotingPage.as_view(), name='create_voting'),
    path('<int:id>/create_questions/', views.create_questions, name='create_questions'),
    path('<int:id>/create_variants/', views.create_variants, name='create_variants'),
    path('<int:id>/', views.voting, name='voting'),
    path('<int:id>/publish/', views.publish_voting, name='publish_voting'),
    path('question/<int:id>/', views.question, name='question'),
]
