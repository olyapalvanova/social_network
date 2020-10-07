from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField

from apps.users.models import User
from apps.common.models import BaseModel


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='post')
    text = models.TextField(null=True, blank=True)
    image = ThumbnailerImageField(null=True, blank=True, upload_to='image/')

    def __str__(self):
        return self.text


class PostComment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    like = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.text


class ChosenPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class ReviewPost(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(null=True, blank=True)
