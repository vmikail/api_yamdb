from rest_framework import serializers
from reviews.models import Category, Genre, Title
import datetime as dt
from rest_framework.validators import UniqueTogetherValidator
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


class TitleSerialiser(serializers.ModelSerializer):
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
        category = CategorySerializer()
        genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = (
            'name', 'year', 'rating', 'description', 'genre', 'category'
        )
