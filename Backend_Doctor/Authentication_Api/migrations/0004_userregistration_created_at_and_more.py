# Generated by Django 5.2 on 2025-04-18 03:27

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication_Api', '0003_userregistration_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregistration',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='userregistration',
            name='date_of_birth',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userregistration',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='male', null=True),
        ),
        migrations.AddField(
            model_name='userregistration',
            name='phone_number',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='userregistration',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to='photo/'),
        ),
    ]
