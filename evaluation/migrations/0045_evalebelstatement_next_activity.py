# Generated by Django 4.0.1 on 2022-05-05 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0044_evaluatoractivities_compulsory_percent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evalebelstatement',
            name='next_activity',
            field=models.BooleanField(default=False),
        ),
    ]