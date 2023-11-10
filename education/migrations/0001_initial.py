# Generated by Django 4.2.7 on 2023-11-10 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название курса')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание курса')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='education/', verbose_name='Превью курса')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название урока')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание урока')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='education/', verbose_name='Превью урока')),
                ('video_link', models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')),
            ],
        ),
    ]