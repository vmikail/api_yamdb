from django.db import models


class Category(models.Model):
    """Перечень возможных типов произведений."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Обозначение'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Genre(models.Model):
    """Перечень жанров произведений."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Обозначение'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Title(models.Model):
    """Произведения."""
    name = models.TextField(
        verbose_name='Название произведения',
        max_length=200
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="title",
        blank=True, null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
    )
    year = models.IntegerField(
        verbose_name='Год выхода'
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        # ordering = ['name']

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE
    )


class Reviews(models.Model):
    """Отзывы на произведения."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name='Произведение'
    )
    text = models.TextField(
        blank=True, null=True,
        verbose_name='Текст отзыва'
    )
    # author = models.ForeignKey(
    #    User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(verbose_name='Оценка')
    pub_date = models.DateTimeField('Дата отзыва', auto_now_add=True)


class Comments(models.Model):
    """Комментарии к отзывам."""
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст комментария')
    # author = models.ForeignKey(
    #    User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField('Дата комментария', auto_now_add=True)
