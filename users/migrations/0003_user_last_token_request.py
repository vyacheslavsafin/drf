# Generated by Django 4.2.7 on 2023-11-23 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_username_user_avatar_user_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_token_request',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]