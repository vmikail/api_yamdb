import datetime as dt

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comments, Genre, Reviews, Title

# from django.db.models import Avg


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('name', 'description', 'year', 'category', 'genre')

    validators = [
        UniqueTogetherValidator(
            queryset=Title.objects.all(),
            fields=('name', 'year')
        )
    ]

    def validate_year(self, value):
        year = dt.date.today().year
        if year < value:
            raise serializers.ValidationError('Проверьте год создания')
        return value


class TitleShowSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True)
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    class Meta:
        model = Reviews
        fields = ('title', 'text', 'score')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('review', 'text')