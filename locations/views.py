from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from django.core.paginator import Paginator
from .models import Post


def home(request):
    posts = Post.objects.all().order_by('-id')
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    post_list = paginator.get_page(page_number)
    return render(request, 'locations/home.html', {'posts': post_list})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'locations/create_post.html', {'form': form})


@login_required()
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'locations/create_post.html', {'form': form, 'edit': True})


@login_required()
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post")
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'locations/confirm_delete.html', {'post': post})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'locations/signup.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('login')


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'locations/post_detail.html', {'post': post})
