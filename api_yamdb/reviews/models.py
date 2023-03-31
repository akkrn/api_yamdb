from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True)
    rating = models.IntegerField(blank=True)
    genre = models.ForeignKey(
        Genre, null=True,
        on_delete=models.SET_NULL,
        related_name='genres',
        verbose_name='Жанр',
        help_text='Жанр, к которому будет относиться релиз'
    )
    category = models.ForeignKey(
        Category, null=True,
        on_delete=models.SET_NULL,
        related_name='categories',
        verbose_name='Категория',
        help_text='Категория, к которой будет относиться релиз'
    )

    def __str__(self):
        return self.name
