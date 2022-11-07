from django.contrib import admin

from .models import Category, Genre, Title


class TitleAdmin(admin.ModelAdmin):
    # позовляет администрировать перечень произведений
    list_editable = ('category',)
    list_display = (
        'pk', 'name', 'year', 'category', 'description')
    search_fields = ('name',)
    list_filter = ('year', 'category',)


class CategoryAdmin(admin.ModelAdmin):
    # позволяет администрировать перечень категорий
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name', 'slug',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    # позволяет администрировать перечень жанров
    list_display = (
        'pk',
        'name',
        'slug',
    )
    search_fields = ('name', 'slug',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
