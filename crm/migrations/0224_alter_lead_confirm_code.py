# Generated by Django 4.0.1 on 2022-12-08 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0223_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='312840286789', max_length=50),
        ),
    ]
