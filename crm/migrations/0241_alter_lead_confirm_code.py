# Generated by Django 4.0.1 on 2023-04-06 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0240_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='708848944573', max_length=50),
        ),
    ]
