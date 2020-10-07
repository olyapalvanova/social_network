from django.contrib import admin
from .models import Post, PostComment, ChosenPost, ReviewPost


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'text')


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text')


class ChosenPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')


class ReviewPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')


admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, PostCommentAdmin)
admin.site.register(ChosenPost, ChosenPostAdmin)
admin.site.register(ReviewPost, ReviewPostAdmin)
