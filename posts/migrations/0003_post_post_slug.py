# Generated by Django 4.2.2 on 2023-06-20 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_slug',
            field=models.SlugField(default='title', verbose_name='post slug'),
            preserve_default=False,
        ),
    ]