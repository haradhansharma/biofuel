# Generated by Django 4.0.1 on 2022-09-17 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0164_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='097986995146', max_length=50),
        ),
    ]
