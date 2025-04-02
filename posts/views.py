from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required
from userProfile.models import Profile

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  
            post.save()  
            return redirect('posts:create_post')  # Redirect to refresh the page after posting

    else:
        form = PostForm()

    # Fetch all posts in descending order
    public_users = Profile.objects.filter(privacy=Profile.PUBLIC).values_list('user', flat=True)
    posts = Post.objects.filter(user__in=public_users).order_by('-created_at')

    return render(request, 'create_post.html', {'form': form, 'posts': posts})

