# Generated by Django 4.0.1 on 2023-03-06 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0234_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='925029092719', max_length=50),
        ),
    ]
