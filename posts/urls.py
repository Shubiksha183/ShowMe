from django.urls import path
from  .views import create_post

app_name = 'posts'

urlpatterns = [
    path('create/', create_post, name='create_post'),  
]