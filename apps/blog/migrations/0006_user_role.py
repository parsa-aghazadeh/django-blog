# Generated by Django 5.1.2 on 2024-10-12 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_rename_save_post_saved'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[('1', 'Admin'), ('2', 'User')], default='2'),
        ),
    ]
