# Generated by Django 4.0.1 on 2022-06-01 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0125_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='775947008382', max_length=50),
        ),
    ]
