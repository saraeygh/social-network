# Generated by Django 4.2.2 on 2023-07-04 10:36

import django.contrib.auth.models
from django.db import migrations, models
import useraccounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccounts', '0020_alter_useraccount_managers_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='useraccount',
            managers=[
                ('objects', useraccounts.models.UserAccountManager()),
                ('objects_all', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='bio',
            field=models.CharField(blank=True, max_length=160, null=True, verbose_name='Bio'),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='user_slug',
            field=models.SlugField(default='4ed6773394324af78af7365510d7484e', unique=True, verbose_name='User slug'),
        ),
    ]
