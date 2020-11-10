from django.contrib import admin
from .models import Organization, News, Category, NewsComment


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class NewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_at')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text')


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(NewsComment, NewsCommentAdmin)
