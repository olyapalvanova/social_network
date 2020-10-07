from django.db import models

from apps.users.models import User


class SocialAuth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.user, self.type
