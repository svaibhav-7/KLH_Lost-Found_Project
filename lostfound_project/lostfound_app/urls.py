# lostfound_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('post/', views.post_item, name='post_item'),
    path('claim/<int:pk>/', views.claim_item, name='claim_item'),
    path('delete/<int:pk>/', views.delete_claimed_item, name='delete_claimed_item'),
    path('signup/', views.signup_view, name='signup'),
]
