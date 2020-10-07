from django.db import models


class BaseModel(models.Model):
    date = models.DateTimeField()

    class Meta:
        abstract = True
