from django.urls import path

from .views import (profile, dialog_list, dialog,
                    user_posts_list, posts, news_list, news, setting, logout,
                    update_profile)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('profile/<int:id>/', profile, name='profile'),
    path('profile/update/', update_profile, name='update'),
    path('dialog/list/', dialog_list, name='dialog_list'),
    path('dialog/', dialog, name='dialog'),
    path('users/<int:id>/posts/', user_posts_list, name='post'),
    path('posts/', posts, name='posts'),
    path('news/list', news_list, name='news_list'),
    path('news', news, name='news'),
    path('setting', setting, name='setting'),
]
