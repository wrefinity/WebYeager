# Generated by Django 4.1.9 on 2023-05-31 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0006_rename_socket_path_worldinstance_default_preview_url_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='worldinstance',
            old_name='default_preview_url',
            new_name='default_preview_file',
        ),
        migrations.AddField(
            model_name='worldinstance',
            name='default_preview_urls',
            field=models.URLField(blank=True, null=True),
        ),
    ]
