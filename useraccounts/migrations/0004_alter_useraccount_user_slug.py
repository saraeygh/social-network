# Generated by Django 4.2.2 on 2023-06-25 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccounts', '0003_alter_useraccount_user_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='user_slug',
            field=models.SlugField(default='7faa0d3115a94769b5fd0260da57fbcf', unique=True, verbose_name='User slug'),
        ),
    ]
