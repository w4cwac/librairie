from django.urls import path
from .views import media_list

urlpatterns = [
    path('medias/', media_list, name='consultation_media_list'),
]