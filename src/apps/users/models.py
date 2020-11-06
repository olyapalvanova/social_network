from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(_('email address'), blank=True, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True, default='')
    school = models.CharField(max_length=100, null=True, blank=True,
                              default='')
    work = models.CharField(max_length=100, null=True, blank=True, default='')
    image = ThumbnailerImageField(null=True, blank=True,
                                  upload_to='avatars/',
                                  resize_source=dict(quality=95,
                                                     size=(2048, 2048),
                                                     sharpen=True))
    description = models.CharField(max_length=100, null=True, blank=True,
                                   default='')
    music = models.CharField(max_length=100, null=True, blank=True, default='')
    books = models.CharField(max_length=100, null=True, blank=True, default='')
    interests = models.CharField(max_length=100, null=True, blank=True,
                                 default='')
    status = models.CharField(max_length=100, null=True, blank=True,
                              default='')
    is_private = models.BooleanField(default=False)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_short_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name} ({self.email})'
        return self.email

    def __str__(self):
        return self.get_short_name()


class Friend(models.Model):
    users = models.ManyToManyField(User, related_name='friends')
    date_added = models.DateField(auto_now_add=True)
    added = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='added_friend')
    permission = models.BooleanField(default=False)
