# Generated by Django 4.0.1 on 2022-07-30 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0147_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='683701569685', max_length=50),
        ),
    ]
