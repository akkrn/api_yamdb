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


class SlugDictRelatedField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        result = {
            "name": obj.name,
            "slug": obj.slug
        }
        return result


class TitleSerializerGet(serializers.ModelSerializer):
    category = SlugDictRelatedField(
        slug_field='slug', read_only=True)
    genre = SlugDictRelatedField(
        slug_field='slug', many=True, read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre',
                  'category', 'rating')
        model = Title


class TitleSerializerPost(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(), many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre',
                  'category', 'rating')
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if not value <= year:
            raise serializers.ValidationError('Проверьте год рождения!')
        return value
