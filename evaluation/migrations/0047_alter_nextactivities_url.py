# Generated by Django 4.0.1 on 2022-05-09 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0046_nextactivities_compulsory_percent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nextactivities',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
