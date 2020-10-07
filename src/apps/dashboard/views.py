from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout

from .forms import UserInfoForm
from apps.posts.models import Post
from apps.users.models import User


def user_login(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'dashboard/profile.html')
    else:
        form = UserCreationForm()
        return render(request, 'registration/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return render(request, 'registration/logout.html')


def profile(request, id):
    user = User.objects.get(id=id)
    form = UserInfoForm(instance=request.user)
    return render(request, 'dashboard/profile.html', {'form': form,
                                                      'account': user})


# TODO: login required
def update_profile(request):
    if request.method == 'POST':
        user = UserInfoForm(request.POST, instance=request.user)
        if user.is_valid():
            user.save()
            return redirect('profile', id=request.user.id)
    user = UserInfoForm(instance=request.user)
    return render(request, 'dashboard/update.html', {'user': user})


def user_posts_list(request, id):
    posts = Post.objects.filter(user_id=id)
    return render(request, 'dashboard/post.html', {'posts': posts})


def dialog_list(request):
    current_page = 'dialog_list'
    return render(request, 'dashboard/dialog_list.html',
                  {'current_page': current_page})


def dialog(request):
    current_page = 'dialog'
    return render(request, 'dashboard/dialog.html',
                  {'current_page': current_page})


def posts(request):
    current_page = 'post'
    return render(request, 'dashboard/posts.html',
                  {'current_page': current_page})


def news_list(request):
    current_page = 'news_list'
    return render(request, 'dashboard/news_list.html',
                  {'current_page': current_page})


def news(request):
    current_page = 'news'
    return render(request, 'dashboard/news.html',
                  {'current_page': current_page})


def setting(request):
    return render(request, 'dashboard/setting.html')
