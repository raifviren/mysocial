# Generated by Django 2.0.1 on 2018-01-22 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20180122_0403'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='insta_access_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='insta_full_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='insta_user_id',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True, unique=True),
        ),
    ]
