from typing import ClassVar

from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    actions: ClassVar = ['rename']

    @admin.action(description="rename it")
    def rename(self, request, queryset):
        queryset.update(title="renamedfine")
