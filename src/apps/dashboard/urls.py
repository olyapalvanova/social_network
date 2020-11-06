from django.urls import path

from .views import (
    profile, dialogs, dialog, user_posts_list, posts, news, news_details,

    setting, logout_user, update_profile, user_login
)

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profiles/<int:id>/', profile, name='profile'),
    path('profile/update/', update_profile, name='update'),
    path('dialogs/', dialogs, name='dialogs'),
    path('dialog/<int:id>/', dialog, name='dialog'),
    path('users/<int:id>/posts/', user_posts_list, name='user_posts_list'),
    path('posts/', posts, name='posts'),
    path('news/', news, name='news'),
    path('news/details', news_details, name='news_details'),
    path('setting', setting, name='setting'),
]
