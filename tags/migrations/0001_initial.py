# Generated by Django 4.2.2 on 2023-06-20 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=20, verbose_name='Tag label')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at:')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at:')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='TaggedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('user', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at:')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at:')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tags.tag')),
                ('tag_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag_from', to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
            },
        ),
    ]
