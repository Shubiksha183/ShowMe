from django.urls   import path

app_name = 'friends'
from .views import send_friend_request, accept_friend_request, friend_list

urlpatterns = [
    path('send/<int:user_id>/', send_friend_request, name='send_request'),
    path('accept/<int:request_id>/', accept_friend_request, name='accept_request'),
    path('', friend_list, name='list'),
]