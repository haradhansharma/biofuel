# Generated by Django 4.0.1 on 2022-09-29 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0183_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='353044897245', max_length=50),
        ),
    ]
