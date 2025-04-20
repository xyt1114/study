"""
URL configuration for 实训后端2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from 实训后端2 import views
from controller import SystemContriller as sc
from controller import MyRobtController as mrc

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/chat/", views.chat_api, name="chat_api"),
    path('favicon.ico', lambda _: HttpResponse(status=204)),
    path('index/',sc.go_index),
    path('logon/',sc.go_logon),
    path('',sc.go_login),
    path('historyList/',mrc.history_list),
    path("question/",mrc.question),
    path("user_logon/",mrc.user_logon),
    path("user_login/",mrc.user_login),
    path("qaList/",mrc.qa_list),

]
