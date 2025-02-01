from django.shortcuts import render
from django.http import HttpResponse
from .models import User

# Create your views here.
def add_user(request):
    user = User.objects.create(
        name='ldj',
        password='123456',
    )

    return HttpResponse(f"User {user.name} created successfully!")

def delete_user(request):
    user = User.objects.get(id=3)
    user.delete()