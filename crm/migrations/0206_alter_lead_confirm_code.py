# Generated by Django 4.0.1 on 2022-11-05 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0205_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='620479285224', max_length=50),
        ),
    ]
