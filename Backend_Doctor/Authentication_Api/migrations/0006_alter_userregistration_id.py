# Generated by Django 5.2 on 2025-04-19 09:50

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication_Api', '0005_alter_userregistration_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregistration',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
