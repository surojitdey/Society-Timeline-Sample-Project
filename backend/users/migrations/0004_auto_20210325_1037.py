# Generated by Django 3.1.7 on 2021-03-25 10:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_familydetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='family_members',
            field=models.IntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='numbers of family members'),
        ),
    ]
