from django.urls import path
from main import views

urlpatterns = [
    path('list/', views.ListVotingsPage.as_view(), name='list_votings'),
    path('create_voting/', views.CreateVotingPage.as_view(), name='create_voting'),
    path('<int:id>/create_questions/', views.CreateQuestionPage.as_view(), name='create_questions'),
    path('<int:id>/create_variants/', views.CreateVariantsPage.as_view(), name='create_variants'),
    path('<int:id>/', views.VotingPage.as_view(), name='voting'),
    path('<int:id>/publish/', views.publish_voting, name='publish_voting'),
    path('question/<int:id>/', views.QuestionPage.as_view(), name='question'),
    path('<int:id>/like/', views.like_voting, name='like'),
]
