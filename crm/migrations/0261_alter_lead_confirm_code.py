# Generated by Django 4.0.1 on 2023-06-21 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0260_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='391335146977', max_length=50),
        ),
    ]