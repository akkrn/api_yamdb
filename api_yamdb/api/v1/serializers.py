import datetime as dt

from rest_framework import serializers

from django.db.models import Avg
from django.forms import ValidationError
from django.shortcuts import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genre


class SlugDictRelatedField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        result = {"name": obj.name, "slug": obj.slug}
        return result


class TitleSerializerGet(serializers.ModelSerializer):
    category = SlugDictRelatedField(slug_field="slug", read_only=True)
    genre = SlugDictRelatedField(slug_field="slug", many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg("score")).get("score__avg")
        return rating if not rating else round(rating, 0)

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
            "rating",
        )
        model = Title


class TitleSerializerPost(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    genre = serializers.SlugRelatedField(
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
            "rating",
        )
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if not value <= year:
            raise serializers.ValidationError("Проверьте год рождения!")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer для отзыва."""

    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.SlugRelatedField(slug_field="name", read_only=True)

    def validate(self, data):
        request = self.context["request"]
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if request.method == "POST":
            if Review.objects.filter(
                title=title, author=request.user
            ).exists():
                raise ValidationError(
                    "Допустимо не более 1 отзыва на произведение"
                )
        return data

    def validate_score(self, score):
        if score < 1 or score > 10:
            raise serializers.ValidationError(
                "Рейтинг произведения должен быть от 1 до 10"
            )
        return score

    class Meta:
        fields = (
            "id",
            "author",
            "title",
            "score",
            "text",
            "pub_date",
        )
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )
    review = serializers.ReadOnlyField(source="review.id")

    class Meta:
        fields = (
            "id",
            "author",
            "review",
            "text",
            "pub_date",
        )
        model = Comment
