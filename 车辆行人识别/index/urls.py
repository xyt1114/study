from django.urls import path

from index import views
from .views import VideoUploadView
from django.urls import path
from .views import VideoUploadView, get_csrf_token


urlpatterns = [
    path("home", views.home),
    path('api/upload/', VideoUploadView.as_view(), name='video-upload'),
    path('api/csrf/', get_csrf_token, name='get-csrf'),
]
