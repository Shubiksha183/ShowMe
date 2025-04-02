from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Friendship
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def send_friend_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    if request.user != receiver and not Friendship.objects.filter(sender=request.user, receiver=receiver).exists():
        Friendship.objects.create(sender=request.user, receiver=receiver)
    return redirect('friends:list')

@login_required
def accept_friend_request(request, request_id):
    friendship = get_object_or_404(Friendship, id=request_id, receiver=request.user)
    friendship.accepted = True
    friendship.save()
    print(f"Friend request accepted: {friendship.sender} → {friendship.receiver}") 
    return redirect('friends:list')

@login_required
def friend_list(request):
    friends = User.objects.filter(
        id__in=Friendship.objects.filter(accepted=True, sender=request.user).values_list('receiver', flat=True)
    ) | User.objects.filter(
        id__in=Friendship.objects.filter(accepted=True, receiver=request.user).values_list('sender', flat=True)
    )

    pending_requests = Friendship.objects.filter(receiver=request.user, accepted=False)

    return render(request, 'friends_list.html', {
        'friends': friends,
        'pending_requests': pending_requests
    })
