# Generated by Django 4.1.9 on 2023-05-28 22:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0004_worldclass_rating_worldratings'),
    ]

    operations = [
        migrations.AddField(
            model_name='worldinstance',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, unique=True),
            preserve_default=False,
        ),
    ]
