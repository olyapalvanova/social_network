from django.db import models

from apps.users.models import User


class Channel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_channels')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_channels')
    notice = models.BooleanField(default=True)
    archived = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)


class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    read = models.BooleanField()
