from django.urls import path
from main import views

urlpatterns = [
    path('list/', views.ListComplainsPage.as_view(), name='complains_list'),
    path('<int:id>/', views.ComplaintPage.as_view(), name='complaint'),
    path('create/<int:id>/', views.CreateComplaintPage.as_view(), name='create_complaint'),
]
