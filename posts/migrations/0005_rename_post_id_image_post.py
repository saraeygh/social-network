# Generated by Django 4.2.2 on 2023-06-25 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_post_post_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='post_id',
            new_name='post',
        ),
    ]
