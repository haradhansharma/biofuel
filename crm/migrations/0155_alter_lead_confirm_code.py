# Generated by Django 4.0.1 on 2022-08-29 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0154_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='017673546980', max_length=50),
        ),
    ]
