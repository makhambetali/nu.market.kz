# Generated by Django 5.1 on 2024-08-26 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='', max_length=255, unique=True, verbose_name='URL'),
            preserve_default=False,
        ),
    ]