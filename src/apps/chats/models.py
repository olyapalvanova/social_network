from os import path

from django.conf import settings
from django.db import models

from apps.users.models import User


class Channel(models.Model):
    DEFAULT_GROUP_LOGO = path.join(settings.MEDIA_URL, 'avatars/unnamed.png')

    users = models.ManyToManyField(User, related_name='channels')
    notice = models.BooleanField(default=True)
    archived = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)

    def partner_logo(self, user):
        base_qs = self.users.exclude(id=user.id)
        if base_qs.count() != 1:
            return self.DEFAULT_GROUP_LOGO
        user_image = base_qs.first().image
        if user_image:
            return user_image.url
        else:
            return self.DEFAULT_GROUP_LOGO

    @property
    def channel_name(self):
        name = ''
        for i in self.users.all():
            name += i.first_name + ' ' + i.last_name + ' '
        return name


class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    read = models.BooleanField(default=False)
