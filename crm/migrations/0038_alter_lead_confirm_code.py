# Generated by Django 4.0.1 on 2022-03-30 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0037_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='822350226655', max_length=50),
        ),
    ]
