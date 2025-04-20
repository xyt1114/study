from django.contrib import admin
from django.urls import path

from user import views
from user.views import LoginView

urlpatterns = [
    path('add', views.add, name='add'),
    path('login',LoginView.as_view(),name='login'),
    path('register',views.register,name='register'),
]