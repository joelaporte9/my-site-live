from argparse import Namespace
from django.urls import path
from . import views
from .views import *\

from django.urls import include, path

urlpatterns = [
    path(' ', views.gallery, name='gallery'),
    path('photo/<str:pk>', views.viewPhoto, name='photo'),
    path('add/', views.add, name='add'),
    path('addGooglePhoto/',views.addPhoto, name='addPhoto'),
    path('addToAlbum/',views.addToAlbum, name='addToAlbum'),
    path('addAlbum',views.addAlbum, name='addAlbum'),
]
 
