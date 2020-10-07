from django.contrib import admin
from .models import SocialAuth


class SocialAuthAdmin(admin.ModelAdmin):
    list_display = ('user', 'type')


admin.site.register(SocialAuth, SocialAuthAdmin)
