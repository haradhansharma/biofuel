# Generated by Django 4.0.1 on 2022-03-21 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0025_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='892246100983', max_length=50),
        ),
    ]
