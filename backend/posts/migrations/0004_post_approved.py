# Generated by Django 3.1.7 on 2021-03-31 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20210331_0701'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='approved'),
        ),
    ]
