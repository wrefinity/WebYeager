# Generated by Django 4.1.9 on 2023-06-01 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0007_rename_default_preview_url_worldinstance_default_preview_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worldinstance',
            name='socket_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
