# Generated by Django 5.1 on 2024-08-11 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_post_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='price',
            field=models.CharField(max_length=15, verbose_name='Стоимость товара'),
        ),
    ]
