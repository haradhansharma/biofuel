# Generated by Django 4.0.1 on 2022-02-27 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0021_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='341798767532', max_length=50),
        ),
    ]
