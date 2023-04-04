from django.contrib import admin

from .models import User
from reviews.models import Category, Genre, Title, Review, Comment

admin.site.register(User)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
    )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "year",
        "description",
        "category",
        "rating",
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'author',
        'pub_date',
        'title',
        'score',
    )


@admin.register(Comment)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'review',
        'text',
        'pub_date',
    )