from django.contrib import admin
from .models import Category, Comment, Genre, Review, Title


class TitleInline(admin.StackedInline):
    model = Title
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (TitleInline,)
    list_display = ('name', 'slug',)
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(CategoryAdmin):
    inlines = ()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'pub_date',)
    search_fields = ('text',)
    list_editable = ('text',)
    list_display_links = ('id',)
    list_filter = ('author', 'pub_date',)


@admin.register(Review)
class ReviewAdmin(CommentAdmin):
    list_display = CommentAdmin.list_display + ('score',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'year', 'category',)
    search_fields = ('name', 'description',)
    list_editable = ('description', )
    list_filter = ('year',)
