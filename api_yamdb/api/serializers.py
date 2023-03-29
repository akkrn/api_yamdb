import datetime as dt
from rest_framework import serializers

from reviews.models import Title, Category, Genre

# CATEGORY_CHOICES = Category.objects.all()
# GENRE_CHOICES = Genre.objects.all()


class TitleSerializer(serializers.ModelSerializer):
    # genre = serializers.ChoiceField(choices=GENRE_CHOICES)
    # category = serializers.ChoiceField(choices=CATEGORY_CHOICES)

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if not value <= year:
            raise serializers.ValidationError('Проверьте год рождения!')
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre
