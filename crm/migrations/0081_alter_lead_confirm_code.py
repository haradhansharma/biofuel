# Generated by Django 4.0.1 on 2022-04-16 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0080_alter_lead_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='confirm_code',
            field=models.CharField(default='766376408198', max_length=50),
        ),
    ]
