# Generated by Django 4.0.1 on 2023-02-18 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0232_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='891803824592', max_length=50),
        ),
    ]
