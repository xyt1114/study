from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def logined(request):
    return HttpResponse('这是个人信息首页')
