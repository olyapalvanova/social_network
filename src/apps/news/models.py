from django.db import models

from apps.users.models import User
from apps.common.models import BaseModel


class Organization(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to='organization/')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class News(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='news/')

    def __str__(self):
        return self.name


class NewsComment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    text = models.TextField()
    like = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.user
