# Generated by Django 5.0.4 on 2024-05-19 08:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asms_app', '0009_alter_reply_repliedby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='examdate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='subclass',
            field=models.CharField(default=1, max_length=3),
        ),
    ]
