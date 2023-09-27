# Generated by Django 4.2.3 on 2023-09-27 15:26

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
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'ordering': ['-created_at', '-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='TaggedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(verbose_name='ID')),
                ('user', models.PositiveIntegerField(verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype', verbose_name='Content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='used_tag', to='tags.tag', verbose_name='Tag')),
                ('tag_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag_from', to='contenttypes.contenttype', verbose_name='Content type')),
            ],
            options={
                'verbose_name': 'Tagged item',
                'verbose_name_plural': 'Tagged items',
                'ordering': ['-created_at', '-updated_at'],
            },
        ),
    ]