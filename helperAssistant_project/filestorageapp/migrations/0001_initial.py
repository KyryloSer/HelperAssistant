# Generated by Django 4.1.3 on 2022-11-22 00:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('file', models.FileField(blank=True, upload_to='helperAssistant_project/')),
                ('size', models.IntegerField(default=0)),
                ('type', models.CharField(max_length=50)),
                ('uploaded_time', models.DateTimeField(default=datetime.datetime(2022, 11, 22, 2, 59, 25, 448493))),
                ('global_bool', models.BooleanField(default=False)),
            ],
        ),
    ]
