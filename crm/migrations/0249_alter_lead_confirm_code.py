# Generated by Django 4.0.1 on 2023-04-27 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0248_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='895046586079', max_length=50),
        ),
    ]