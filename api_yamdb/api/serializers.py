from rest_framework import serializers
from reviews.models import Category, Genre, Title
import datetime as dt
# from rest_framework.validators import UniqueTogetherValidator


class TitleSerialiser(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'

    # validators = [
    #     UniqueTogetherValidator(
    #         queryset=Title.objects.all(),
    #         fields=('name', 'year')
    #     )
    # ]

    def validate_year(self, value):
        year = dt.date.today().year
        if year < value:
            raise serializers.ValidationError('Проверьте год создания')
        return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
