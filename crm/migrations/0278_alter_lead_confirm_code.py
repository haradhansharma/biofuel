# Generated by Django 4.0.1 on 2023-10-19 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0277_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='706815697379', max_length=50),
        ),
    ]