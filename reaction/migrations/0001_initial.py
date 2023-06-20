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
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction_status', models.CharField(choices=[('LIKE', 'Like'), ('DISLIKE', 'Dislike')], max_length=50)),
                ('object_id', models.PositiveIntegerField()),
                ('user', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at:')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at:')),
                ('reaction_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('reaction_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reaction_from', to='contenttypes.contenttype')),
            ],
        ),
    ]
