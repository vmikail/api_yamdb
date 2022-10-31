from django.db import models


class Category(models.Model):
    """Перечень возможных категорий произведений."""
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Обозначение'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Genre(models.Model):
    """Перечень жанров произведений."""
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Обозначение'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['title']


class Title(models.Model):
    """Произведения."""
    title = models.TextField(
        verbose_name='Название произведения',
        max_length=200)
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

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['title']


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
