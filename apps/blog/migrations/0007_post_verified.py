# Generated by Django 5.1.2 on 2024-10-12 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
