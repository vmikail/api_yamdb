# Generated by Django 2.2.19 on 2022-11-04 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20221104_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.IntegerField(default=None, null=True, verbose_name='Рейтинг'),
        ),
    ]