# Generated by Django 4.0.1 on 2022-11-05 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0079_olilist_remove_stdoils_name_stdoils_select_oil'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='standaredchart',
            name='key',
        ),
        migrations.RemoveField(
            model_name='standaredchart',
            name='related_biofuel',
        ),
        migrations.AddField(
            model_name='olilist',
            name='key',
            field=models.CharField(blank=True, editable=False, max_length=250, null=True),
        ),
    ]
