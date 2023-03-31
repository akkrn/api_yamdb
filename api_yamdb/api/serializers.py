import datetime as dt
from rest_framework import serializers

from reviews.models import Title, Category, Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if not value <= year:
            raise serializers.ValidationError('Проверьте год рождения!')
        return value

    def validate_category(self, value):
        if str(Category.objects.filter(slug=value).last().slug) == str(value):
            return value
        raise serializers.ValidationError('Категории не существует')

    def validate_genre(self, value):
        if str(Genre.objects.filter(slug=value).last().slug) == str(value):
            return value
        raise serializers.ValidationError('Жанра не существует')
