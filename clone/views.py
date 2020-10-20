# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect,get_object_or_404,reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from annoying.decorators import ajax_request
from .forms import PhotoUploadModelForm,CommentForm,ProfileEditForm
#Sfrom friendship.models import Friend, Follow, Block
from django.contrib.auth.decorators import login_required

from .models import Image,Comment
from Users.models import User,Profile


def home(request):
    posts= Image.objects.all(),
    commentform= CommentForm()

    return render(request, 'index.html', locals())

class PostListView(LoginRequiredMixin,ListView):
    model=Image
    template_name= 'clone/image_list.html'

    context_object_name = 'posts'
    ordering = ['-time_created']




class PostCreateView(LoginRequiredMixin,CreateView):
    form_class = PhotoUploadModelForm
    template_name = 'clone/image_upload.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.user_profile= self.request.user.profile
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Image
    fields = ['title', 'content']

class create_comment(CreateView):
    model=Comment
    template_name= 'clone/image_list.html'

    context_object_name = 'comments'
    ordering = ['-posted_on']

def signout(request):
    logout(request)
    return redirect('login')



def add_comment(request,post_id):
    post = get_object_or_404(Image, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect('home')


@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'searchItem' in request.GET and request.GET["searchItem"]:
        search_term = request.GET.get("searchItem")
        searched_user = Profile.search_by_username(search_term)
        message = f"{search_term}"
        context = {
            'message': message,
            'searched_user': searched_user
        }
        return render(request, 'search.html', context)

    else:
        message = "You haven't searched for any term"
        return render(request, 'index.html',{"message":message})

@login_required(login_url='/accounts/login/')
def profile(request, username):
    user = User.objects.get(username=username)
    if not user:
        return redirect('home')

    profile = Profile.objects.get(user=user)
    context = {
        'username': username,
        'user': user,
        'profile': profile
    }
    print(profile.user.username)
    print(profile.image)
    return render(request, 'clone/profile.html', context)
@login_required(login_url='/accounts/login/')
def post(request, pk):
    post = Image.objects.get(pk=pk)
    try:
        like = Like.objects.get(post=post, user=request.user)
        liked = 1
    except:
        like = None
        liked = 0

    context = {
        'post': post,
        'liked': liked
    }
    return render(request, 'clone/post.html', context)


def likes(request, pk):
    post = Image.objects.get(pk=pk)
    profiles = Like.objects.filter(post=post)

    context = {
        'header': 'Likes',
        'profiles': profiles
    }
    return render(request, 'clone/follow_list.html', context)


def followers(request, username):
    user = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user)
    profiles = user_profile.followers.all

    context = {
        'header': 'Followers',
        'profiles': profiles,
    }

    return render(request, 'clone/follow_list.html', context)

@login_required(login_url='/accounts/login/')
def following(request, username):
    user = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user)
    profiles = user_profile.following.all

    context = {
        'header': 'Following',
        'profiles': profiles
    }
    return render(request, 'clone/follow_list.html', context)
@login_required(login_url='/accounts/login/')
def profile_settings(request, username):
    user = User.objects.get(username=username)
    if request.user != user:
        return redirect('index')

    if request.method == 'POST':
        print(request.POST)
        form = ProfileEditForm(request.POST, instance=user.profile, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile', kwargs={'username': user.username}))
    else:
        form = ProfileEditForm(instance=user.profile)

    context = {
        'user': user,
        'form': form
    }
    return render(request, 'clone/profile_settings.html', context)


def follow(request,user_id):
    res = AjaxFollow(request.Get,request.user)
    context = { 'ajax_output': ajax_output()}
    return render(request,'clone/profile.html',context)
