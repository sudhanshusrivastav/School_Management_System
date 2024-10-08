# Generated by Django 5.0.4 on 2024-05-19 04:42

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asms_app', '0005_alter_teacherattendance_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homework', models.CharField(max_length=100)),
                ('desc', models.TextField(default='Regular Homework')),
                ('submit_till', models.DateField(default=django.utils.timezone.now)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='asms_app.student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='asms_app.teacher')),
            ],
            options={
                'ordering': ['submit_till'],
            },
        ),
    ]
