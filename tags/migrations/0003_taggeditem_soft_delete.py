# Generated by Django 4.2.2 on 2023-06-19 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_tag_soft_delete'),
    ]

    operations = [
        migrations.AddField(
            model_name='taggeditem',
            name='soft_delete',
            field=models.BooleanField(default=False),
        ),
    ]
