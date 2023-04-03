from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


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
    rating = models.IntegerField(blank=True, null=True, default=None)
    genre = models.ManyToManyField(
        Genre,
        related_name='genres',
        verbose_name='Жанры',
        help_text='Жанр, к которму будет относиться релиз')
    category = models.ForeignKey(
        Category, null=True,
        on_delete=models.SET_NULL,
        related_name='categories',
        verbose_name='Категория',
        help_text='Категория, к которой будет относиться релиз'
    )

    def __str__(self):
        return self.name

class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.IntegerField(validators=[MinValueValidator(1),
                                MaxValueValidator(10)],
                                verbose_name='Оценка'
                                )

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_relationships'
            ),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('id', )
