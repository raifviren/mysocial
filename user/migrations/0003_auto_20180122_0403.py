# Generated by Django 2.0.1 on 2018-01-22 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20180120_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='twitter_oauth_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='twitter_oauth_token_secret',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='twitter_screen_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='twitter_user_id',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True, unique=True),
        ),
    ]
