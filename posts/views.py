from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required
from userProfile.models import Profile
from friends.models import Friendship  # Import Friendship model
from django.db import models

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  
            post.save()  
            return redirect('posts:create_post')  # Refresh page after posting

    else:
        form = PostForm()

    # Fetch public users
    public_users = Profile.objects.filter(privacy=Profile.PUBLIC).values_list('user', flat=True)

    # Fetch private users who are friends with the logged-in user
    friends = Friendship.objects.filter(
        (models.Q(sender=request.user) | models.Q(receiver=request.user)), accepted=True
    ).values_list('sender', 'receiver')

    # Extract unique friend IDs
    friend_ids = set()
    for sender, receiver in friends:
        if sender != request.user.id:
            friend_ids.add(sender)
        if receiver != request.user.id:
            friend_ids.add(receiver)

    # Fetch posts from public users + friends who are private
    posts = Post.objects.filter(
        models.Q(user__in=public_users) | models.Q(user__in=friend_ids)
    ).order_by('-created_at')

    return render(request, 'create_post.html', {'form': form, 'posts': posts})
