from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('bio', 'role',)}),
    )


class TitleInline(admin.StackedInline):
    model = models.Title
    extra = 1


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (TitleInline,)
    list_display = ('name', 'slug',)
    search_fields = ('name',)


@admin.register(models.Genre)
class GenreAdmin(CategoryAdmin):
    inlines = ()


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'pub_date',)
    search_fields = ('text',)
    list_editable = ('text',)
    list_display_links = ('id',)
    list_filter = ('author', 'pub_date',)


@admin.register(models.Review)
class ReviewAdmin(CommentAdmin):
    list_display = CommentAdmin.list_display + ('score',)


@admin.register(models.Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'year', 'category',)
    search_fields = ('name', 'description',)
    list_editable = ('description', )
    list_filter = ('year',)
