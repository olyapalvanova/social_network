from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login

from .forms import UserForm, UserLoginForm
from apps.posts.models import Post
from apps.chats.models import Message
from apps.users.models import User


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard:news')
    else:
        form = UserLoginForm()

    return render(request, 'registration/login.html', context={'form': form})


def logout_user(request):
    logout(request)
    return redirect('dashboard:login')


@login_required
def profile(request, id):
    user = User.objects.get(id=id)
    return render(request, 'dashboard/profile.html', {'account': user})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('dashboard:profile', id=request.user.id)
        return render(request, 'dashboard/update.html', {'form': form})
    form = UserForm(instance=request.user)
    return render(request, 'dashboard/update.html', {'form': form})


@login_required
def user_posts_list(request, id):
    posts = Post.objects.filter(user_id=id)
    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'dashboard/post.html', {'page': page})


@login_required
def dialogs(request):
    channels = request.user.channels.all()
    for channel in channels:
        channel.logo = channel.partner_logo(user=request.user)
    return render(request, 'dashboard/dialog_list.html', {
        'channels': channels
    })


@login_required
def dialog(request, id):
    messages = Message.objects.filter(channel_id=id)
    paginator = Paginator(messages, settings.MESSAGE_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'dashboard/dialog.html', {'page': page})


@login_required
def posts(request):
    return render(request, 'dashboard/posts.html')


@login_required
def news(request):
    return render(request, 'dashboard/news_list.html')


@login_required
def news_details(request):
    return render(request, 'dashboard/news.html')


@login_required
def setting(request):
    return render(request, 'dashboard/setting.html')
