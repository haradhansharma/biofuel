# Generated by Django 4.0.1 on 2022-06-01 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0124_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='550077756864', max_length=50),
        ),
    ]
