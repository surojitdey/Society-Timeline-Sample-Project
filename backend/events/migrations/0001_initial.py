# Generated by Django 3.1.7 on 2021-05-06 10:41

from django.db import migrations, models
import events.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.TextField(max_length=20000, verbose_name='description')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('media_file', models.FileField(blank=True, upload_to=events.models.events_directory_path)),
                ('event_date', models.DateField()),
                ('event_time', models.CharField(blank=True, max_length=2, verbose_name='event time')),
                ('time_convention', models.CharField(blank=True, choices=[('am', 'am'), ('pm', 'pm')], max_length=2, verbose_name='time convention')),
            ],
        ),
    ]
