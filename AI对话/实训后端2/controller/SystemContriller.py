#定义接口，用于访问index.html文件
from django.shortcuts import render


def go_index(request):
    return render(request, 'index.html')

def go_login(request):
    return render(request, 'login.html')

def go_logon(request):
    return render(request, 'logon.html')