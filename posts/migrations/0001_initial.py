# Generated by Django 4.2.2 on 2023-06-19 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soft_delete', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at:')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at:')),
                ('title', models.CharField(max_length=255, verbose_name='Post title')),
                ('content', models.TextField(verbose_name='Post content')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soft_delete', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at:')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at:')),
                ('content', models.TextField(verbose_name='Reply text')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
                ('reply_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.reply')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soft_delete', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at:')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at:')),
                ('image', models.FileField(upload_to='postpic/', verbose_name='Post image(s)')),
                ('alt_text', models.TextField(verbose_name='Image alt')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post', verbose_name='Image for post')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
            },
        ),
    ]