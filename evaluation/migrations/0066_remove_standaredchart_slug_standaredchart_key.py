# Generated by Django 4.0.1 on 2022-10-14 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0065_standaredchart_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='standaredchart',
            name='slug',
        ),
        migrations.AddField(
            model_name='standaredchart',
            name='key',
            field=models.CharField(blank=True, editable=False, max_length=250, null=True),
        ),
    ]
