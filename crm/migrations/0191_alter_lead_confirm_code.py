# Generated by Django 4.0.1 on 2022-10-12 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0190_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='130413215045', max_length=50),
        ),
    ]
