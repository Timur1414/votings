from django.urls import path
from main import views

urlpatterns = [
    path('list/', views.list_votings_page, name='list_votings'),
]
