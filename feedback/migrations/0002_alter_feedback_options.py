# Generated by Django 4.0.1 on 2023-08-31 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'ordering': ('-created_at',)},
        ),
    ]