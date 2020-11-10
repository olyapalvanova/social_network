from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    date_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        abstract = True
