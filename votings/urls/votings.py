from django.urls import path
from main import views

urlpatterns = [
    path('list/', views.ListVotingsPage.as_view(), name='list_votings'),
]
