# Generated by Django 4.2.2 on 2023-07-04 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccounts', '0021_alter_useraccount_managers_alter_useraccount_bio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='user_slug',
            field=models.SlugField(default='34c200c2c9ca46a2b85becb58019365d', unique=True, verbose_name='User slug'),
        ),
    ]
