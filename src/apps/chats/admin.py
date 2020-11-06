from django.contrib import admin
from .models import Message, Channel


class ChannelAdmin(admin.ModelAdmin):
    list_display = ('notice', 'channel_name')
    filter_horizontal = ('users',)


class MassageAdmin(admin.ModelAdmin):
    list_display = ('channel', 'read')


admin.site.register(Message, MassageAdmin)
admin.site.register(Channel, ChannelAdmin)
