# Generated by Django 4.1.9 on 2023-05-28 00:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agent', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentclass',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='AgentRatings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('world', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='agent.agentclass')),
            ],
            options={
                'unique_together': {('world', 'user')},
            },
        ),
    ]