from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator


from reviews.models import Category, Comments, Genre, Review, Title
from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all())]
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Выбрано недопустимое имя.')
        return value

    class Meta:
        fields = ('username', 'email')
        model = User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'role', 'bio')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)
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
        fields = '__all__'
        read_only_fields = ['rating']

    validators = [
        UniqueTogetherValidator(
            queryset=Title.objects.all(),
            fields=('name', 'year')
        )
    ]


class TitleShowSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='review__score__avg', read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    score = serializers.ChoiceField(choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        title = self.context['request'].parser_context['kwargs']['title']
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                    title=title,
                    author=self.context['request'].user
            ).exists():
                raise serializers.ValidationError(
                    'Можно оставить только один отзыв на произведение')
        return data


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comments
        fields = ('id', 'review', 'text', 'author', 'pub_date')
