# lostfound_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/', views.post_item, name='post_item'),
    path('claim/<int:pk>/', views.claim_item, name='claim_item'),
]
