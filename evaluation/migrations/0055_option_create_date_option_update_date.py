# Generated by Django 4.0.1 on 2022-05-24 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0054_evalebelstatement_update_date_evaluator_update_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='option',
            name='update_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
