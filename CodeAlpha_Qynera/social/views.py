from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import RegisterForm, PostForm, CommentForm, ProfileForm
from .models import Post, Comment, Like, Follow, Profile


def register(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('feed')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


class SocialLoginView(LoginView):
    template_name = 'registration/login.html'


@login_required
def feed(request):
    """Home feed: posts from everyone, newest first, with a quick post form."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post published!')
            return redirect('feed')
    else:
        form = PostForm()

    posts = Post.objects.select_related('author', 'author__profile').prefetch_related('likes', 'comments')
    comment_form = CommentForm()
    liked_post_ids = set(
        Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    )
    return render(request, 'social/feed.html', {
        'posts': posts,
        'form': form,
        'comment_form': comment_form,
        'liked_post_ids': liked_post_ids,
    })


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.all()
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    liked_post_ids = set(
        Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    )
    return render(request, 'social/profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
        'liked_post_ids': liked_post_ids,
    })


@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'social/edit_profile.html', {'form': form})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()
    comments = post.comments.select_related('author')
    is_liked = post.is_liked_by(request.user)
    return render(request, 'social/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'is_liked': is_liked,
    })


@login_required
@require_POST
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'like_count': post.like_count()})
    return redirect(request.META.get('HTTP_REFERER', 'feed'))


@login_required
@require_POST
def toggle_follow(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        return HttpResponseForbidden("You can't follow yourself.")

    follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        follow.delete()
        following = False
    else:
        following = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'following': following,
            'follower_count': target.profile.follower_count(),
        })
    return redirect('profile', username=username)


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('feed')
    return render(request, 'social/confirm_delete.html', {'post': post})
