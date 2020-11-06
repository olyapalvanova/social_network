from typing import Union

from apps.users.models import User, Friend


def page_paginator(queryset, page=1, page_size=2):
    count = queryset.count()
    start_index = (page - 1) * page_size
    end_index = page_size * page
    next_page = page + 1
    previous_page = page - 1
    if previous_page == 0:
        previous_page = None
    if count <= end_index:
        next_page = None
    return {
        'count': count,
        'next': next_page,
        'previous': previous_page,
        'results': queryset[start_index:end_index]
    }


def are_friends(user1: User, user2: Union[User, int]) -> bool:
    if isinstance(user2, int):
        user_id = user2
    elif isinstance(user2, User):
        user_id = user2.id
    else:
        raise Exception('invalid variable type')
    exists = Friend.objects.filter(
        id__in=user1.friends.values_list('id'),
        users__id=user_id,
    ).exists()
    return exists
