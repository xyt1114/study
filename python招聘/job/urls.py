from django.urls import path
from job import views

urlpatterns = [
    path('add', views.add_job, name='add_job'),
    path('add1', views.insert_from_file, name='insert_from_file'),
]
