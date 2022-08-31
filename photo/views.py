from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Category, Photo, createAlbum
from django.shortcuts import render, redirect
from photo.init_Photo_Service import service
from django.http import JsonResponse
import pandas as pd 
import requests
import pickle 
import os

def gallery(request):
    categories = Category.objects.all()

    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.filter()
        category = "All Photos"
    else:
        photos = Photo.objects.filter(category__name=category)

    context = {'categories': categories,'category': category, 'photos': photos}
    return render(request, 'photos/gallery.html', context)

def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photos.html', {'photo': photo})

def add(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
       
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
            )
        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)
     
def addToAlbum(request):
    album = createAlbum.objects.all()
    
    if request.method == 'POST':
        'https://photoslibrary.googleapis.com/v1/albums/'+ str(album) +':batchAddMediaItems'
        add_album_request_body  = {
                        'mediaItemIds': [
                            album,
                        ]
                    }
        service.albums().batchAddMediaItems(albumId=str(album),body=add_album_request_body).execute()

    context = {'album': album}
    return render(request, 'photos/addToAlbum.html', context)

def addAlbum(request):
    album = createAlbum.objects.all()
    if request.method == 'POST':
        title = request.POST['title_new']
        title_request_body = {'album': {'title': title}}
        title = createAlbum.objects.create(
            title=title
        )
        service.albums().create(body=title_request_body).execute()

    context = {'album': album}
    return render(request, 'photos/addAlbum.html', context)

def addPhoto(request):
    photo= Photo.objects.all()
    image_dir =  os.path.join(os.getcwd(), '/Users/joelaporte/Downloads/')
    upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'
    token = pickle.load(open('token_photoslibrary_v1.pickle', 'rb'))
    header = {
        "Authorization": 'Bearer ' + token.token,
        "Content-type": "application/octet-stream",
        "X-Goog-Upload-Protocol": "raw" 
    }
    if request.method == 'POST':
        data = request.POST
        googleImage = request.FILES['image']
        googleImageStr = str(googleImage)
        image_file = os.path.join(image_dir, googleImageStr)

        img = open(image_file, 'rb').read()
        response = requests.post(upload_url, data=img, headers=header)

        image_request_body  = {
                    'newMediaItems': [
                        {
                            'description': data['description'],
                            'simpleMediaItem': {
                                'uploadToken': response.content.decode('utf-8')
                            }
                        }
                    ]
                }
        service.mediaItems().batchCreate(body=image_request_body).execute()

    context = {'photo': photo}
    return render(request, 'photos/addGooglePhoto.html', context)







    












