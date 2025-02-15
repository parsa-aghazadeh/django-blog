# Generated by Django 5.1.2 on 2024-10-11 13:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='save',
            field=models.ManyToManyField(related_name='user_save_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
