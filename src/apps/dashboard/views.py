import json

from django.conf import settings
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Count, Exists, OuterRef
from django.db.models import Q

from apps.chats.models import Message, Channel
from apps.posts.models import Post
from apps.users.models import User, Friend
from .forms import UserForm, UserLoginForm, MessageForm, MessageFormFriend
from .utils import are_friends, page_paginator


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

    return render(request, 'registration/login.html', context={
        'form': form,
        'site_title': 'Login | Social Network'})


def logout_user(request):
    logout(request)
    return redirect('dashboard:login')


@login_required
def profile(request, id):
    user = User.objects.annotate(is_friend=Exists(
        Friend.objects.filter(
            id__in=request.user.friends.values_list('id'),
            users__id=OuterRef('id')))
    ).get(id=id)
    friends = request.user.friends.all()
    return render(request, 'dashboard/profile.html',
                  {'account': user, 'friends': friends,
                   'site_title': 'Profile | Social Network'
                   })


@login_required
def friend_dialog(request, user_id):
    channel = Channel.objects.annotate(total_users=Count('users')).\
        filter(users__id=request.user.id).filter(users__id=user_id). \
        filter(total_users=2).first()
    if channel:
        return redirect('dashboard:dialog', id=channel.id)

    # if channel does not exist, we are trying to send first message
    # before creating
    if request.method == 'POST':
        form = MessageFormFriend(request.POST)
        if form.is_valid():
            channel = Channel.objects.create()
            channel.users.add(request.user.id, user_id)
            message = form.save(commit=False)
            message.user_id = request.user.id
            message.channel_id = channel.id
            message.save()
            return redirect('dashboard:dialog', id=channel.id)
        return render(request, 'dashboard/new_channel.html',
                      {'form': form,
                       'id': user_id,
                       'site_title': 'Dialog | Social Network'})
    form = MessageFormFriend()
    return render(request, 'dashboard/new_channel.html',
                  {'form': form,
                   'id': user_id,
                   'site_title': 'Dialog | Social Network'})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard:profile', id=request.user.id)
        return render(request, 'dashboard/update.html', {
            'form': form,
            'site_title': 'Profile | Social Network'})
    form = UserForm(instance=request.user)
    return render(request, 'dashboard/update.html', {
        'form': form,
        'site_title': 'Update | Social Network'})


@login_required
def user_posts_list(request, id):
    posts = Post.objects.filter(user_id=id)
    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'dashboard/post.html', {
        'page': page,
        'site_title': 'Posts | Social Network'})


@login_required
def dialogs(request):
    channels = request.user.channels.filter(blocked=False)
    for channel in channels:
        channel.logo = channel.partner_logo(user=request.user)
    return render(request, 'dashboard/dialog_list.html', {
        'channels': channels, 'is_blocked': False,
        'site_title': 'Dialogs | Social Network'
    })


def dialogs_block(request):
    channels = request.user.channels.filter(blocked=True)
    for channel in channels:
        channel.logo = channel.partner_logo(user=request.user)
    return render(request, 'dashboard/dialog_list.html', {
        'channels': channels, 'is_block': True,
        'site_title': 'Dialogs | Social Network'
    })


@login_required
def switch_block_dialog(request, id):
    if request.method == 'POST' and request.is_ajax():
        channel = Channel.objects.get(id=id)
        channel.blocked = not channel.blocked
        channel.save()
        return JsonResponse({
            'channel_id': channel.id
        })
    return JsonResponse(status=400)


@login_required
def dialog(request, id):
    messages = Message.objects.filter(channel_id=id,
                                      channel__users__id=request.user.id).order_by(
        'id')
    paginator = Paginator(messages, settings.MESSAGE_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'dashboard/dialog.html', {
        'page': page,
        'channel_id': id,
        'site_title': 'Profile | Social Network'
    })


@login_required
def create_group_chat(request):
    if request.method == 'POST' and request.is_ajax():
        request_dict = json.loads(request.body)
        users_list = request_dict.get('user_list', [])
        users_list.append(request.user.id)
        channel = Channel.objects.create()
        channel.users.add(*users_list)
        return JsonResponse({
            'channel_id': channel.id
        })
    return JsonResponse(status=400)


@login_required
def send_message(request):
    if request.method == 'POST' and request.is_ajax():
        # TODO: wrap this expression into try/except
        data = json.loads(request.body)
        form = MessageForm(data=data)
        if form.is_valid():
            channel = form.cleaned_data['channel']
            if not channel.users.filter(id=request.user.id).exists():
                return HttpResponse(status=400)

            message = form.save(commit=False)
            message.user = request.user
            message.save()
            return JsonResponse({
                'text': message.text,
                'user': {
                    'id': message.user.id,
                    'image': message.user.image['avatar'].url,
                    'email': message.user.email,
                }
            })
    return JsonResponse(status=400)


@login_required
def messages_api(request, id):
    # /
    # /?page=1
    # /?page=10
    # /?page=0
    page = request.GET.get('page', 1)
    page = int(page)
    messages = Message.objects.filter(channel_id=id,
                                      channel__users__id=request.user.id)
    page = page_paginator(messages, page=page)
    messages = page['results']
    data = []
    for message in messages:
        data.append({
            'id': message.channel_id,
            'user': {
                'id': message.user.id,
                'image': request.build_absolute_uri(
                    message.user.image
                ),
                'email': message.user.email,
            },
            'text': message.text,
        })
    page['results'] = data
    return JsonResponse(page, safe=False, json_dumps_params={'indent': 2})


@login_required
def posts(request):
    return render(request, 'dashboard/posts.html',
                  {'site_title': 'Posts | Social Network'})


@login_required
def news(request):
    return render(request, 'dashboard/news_list.html',
                  {'site_title': 'News | Social Network'})


@login_required
def profiles(request):
    users = User.objects.exclude(id=request.user.id).annotate(
        is_friend=Exists(
            Friend.objects.filter(
                id__in=request.user.friends.values_list('id'),
                users__id=OuterRef('id'),
            )
        ),
        is_friend_blocked=Exists(
            Friend.objects.filter(
                id__in=request.user.friends.values_list('id'),
                users__id=OuterRef('id'),
                permission=True
            )
        ),
    )
    search_query = request.GET.get('name', '')
    if search_query:
        users = users.filter(Q(first_name__icontains=search_query) | Q(
            last_name__icontains=search_query) | Q(
            birth_date__icontains=search_query) | Q(
            city__icontains=search_query))
    return render(request, 'dashboard/profiles.html', {
        'profiles': users,
        'site_title': 'Profiles | Social Network'
    })


@login_required
def friends_list(request):
    friends = request.user.friends.all()
    return render(request, 'dashboard/profile.html', {
        'friends': friends,
        'site_title': 'Friends | Social Network' })


@login_required
def friend_add(request, user_id):
    friends = are_friends(request.user, user_id)
    if not friends:
        friend = Friend.objects.create(added_id=request.user.id)
        friend.users.add(request.user.id, user_id)
        return redirect('dashboard:profile', id=user_id)
    return redirect('dashboard:profiles')


@login_required
def friend_delete(request, user_id):
    friends = are_friends(request.user, user_id)
    if friends:
        friend = Friend.objects.get(users__id=user_id)
        if friend.id != request.user.id:
            friend.delete()
        return redirect('dashboard:profile', id=request.user.id)
    return redirect('dashboard:profiles')


@login_required
def friend_block(request, user_id):
    friends = are_friends(request.user, user_id)
    if friends:
        friend = Friend.objects.get(users__id=user_id, permission=False)
        if friend.id != request.user.id:
            friend.permission = True
            friend.save()
        return redirect('dashboard:profile', id=request.user.id)
    return redirect('dashboard:profiles')


@login_required
def friend_unblock(request, user_id):
    friends = are_friends(request.user, user_id)
    if friends:
        friend = Friend.objects.get(users__id=user_id, permission=True)
        if friend.id != request.user.id:
            friend.permission = False
            friend.save()
        return redirect('dashboard:profile', id=request.user.id)
    return redirect('dashboard:profiles')


@login_required
def news_details(request):
    return render(request, 'dashboard/news.html',
                  {'site_title': 'News | Social Network'})


@login_required
def setting(request):
    return render(request, 'dashboard/setting.html',
                  {'site_title': 'Setting | Social Network'})
