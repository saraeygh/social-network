# Generated by Django 4.2.2 on 2023-06-27 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccounts', '0010_alter_useraccount_user_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='user_slug',
            field=models.SlugField(default='username', unique=True, verbose_name='User slug'),
        ),
    ]
