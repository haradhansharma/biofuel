# Generated by Django 4.0.1 on 2022-03-30 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0058_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='704840755042', max_length=50),
        ),
    ]
