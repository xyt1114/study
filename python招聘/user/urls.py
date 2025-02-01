from django.urls import path
from user import views

urlpatterns = [
    path('',views.add_user,name='user'),
    path('delete',views.delete_user,name='delete'),
]
