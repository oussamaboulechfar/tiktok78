from django.urls import path
from . import views

urlpatterns = [
    path('', views.vote_page, name='vote'),
    path('login/', views.login_page, name='login'),
]
