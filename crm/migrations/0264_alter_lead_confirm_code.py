# Generated by Django 4.0.1 on 2023-08-31 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0263_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='553681028230', max_length=50),
        ),
    ]
